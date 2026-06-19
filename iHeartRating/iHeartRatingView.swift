import UIKit

@objc public protocol HeartRatingViewDelegate: AnyObject {
    @objc(heartRatingView:didUpdate:)
    func heartRatingView(_ ratingView: HeartRatingView, didUpdate rating: Float)

    @objc(heartRatingView:isUpdating:)
    optional func heartRatingView(_ ratingView: HeartRatingView, isUpdating rating: Float)
}

@IBDesignable
@objcMembers
open class HeartRatingView: UIView {
    public weak var delegate: HeartRatingViewDelegate?

    private var emptyImageViews: [UIImageView] = []
    private var fullImageViews: [UIImageView] = []

    @IBInspectable public var emptyImage: UIImage? {
        didSet {
            emptyImageViews.forEach { $0.image = emptyImage }
            invalidateIntrinsicContentSize()
            setNeedsLayout()
            refresh()
        }
    }

    @IBInspectable public var fullImage: UIImage? {
        didSet {
            fullImageViews.forEach { $0.image = fullImage }
            invalidateIntrinsicContentSize()
            setNeedsLayout()
            refresh()
        }
    }

    public var imageContentMode: UIView.ContentMode = .scaleAspectFit {
        didSet {
            emptyImageViews.forEach { $0.contentMode = imageContentMode }
            fullImageViews.forEach { $0.contentMode = imageContentMode }
            setNeedsLayout()
        }
    }

    @IBInspectable public var minRating: Int = 0 {
        didSet {
            let normalized = min(max(minRating, 0), maxRating)
            if minRating != normalized {
                minRating = normalized
            }
            rating = boundedRating(rating)
            updateAccessibilityState()
        }
    }

    @IBInspectable public var maxRating: Int = 5 {
        didSet {
            let normalized = min(max(maxRating, 1), Self.maximumRatingCount)
            if maxRating != normalized {
                maxRating = normalized
            }
            if minRating > maxRating {
                minRating = maxRating
            }
            guard maxRating != oldValue else {
                updateAccessibilityState()
                return
            }

            removeImageViews()
            initImageViews()
            invalidateIntrinsicContentSize()
            setNeedsLayout()
            rating = boundedRating(rating)
            refresh()
        }
    }

    @IBInspectable public var minImageSize: CGSize = CGSize(width: 5, height: 5) {
        didSet {
            let normalized = CGSize(
                width: finiteNonnegative(minImageSize.width),
                height: finiteNonnegative(minImageSize.height)
            )
            if minImageSize != normalized {
                minImageSize = normalized
            }
            invalidateIntrinsicContentSize()
            setNeedsLayout()
        }
    }

    @IBInspectable public var rating: Float = 0 {
        didSet {
            let normalized = boundedRating(rating)
            if rating != normalized {
                rating = normalized
            }
            if normalized != oldValue {
                refresh()
            }
            updateAccessibilityState()
        }
    }

    @IBInspectable public var editable: Bool = true {
        didSet {
            updateAccessibilityState()
        }
    }

    @IBInspectable public var halfRatings: Bool = false
    @IBInspectable public var floatRatings: Bool = false
    @IBInspectable public var shouldBounce: Bool = false

    public override init(frame: CGRect) {
        super.init(frame: frame)
        initializeControl()
    }

    public required init?(coder: NSCoder) {
        super.init(coder: coder)
        initializeControl()
    }

    public override var intrinsicContentSize: CGSize {
        guard let emptyImage, let fullImage else {
            return .zero
        }

        let imageWidth = max(emptyImage.size.width, fullImage.size.width)
        let imageHeight = max(emptyImage.size.height, fullImage.size.height)
        let itemWidth = min(
            max(finiteNonnegative(imageWidth), minImageSize.width),
            Self.maximumSafeDimension
        )
        let itemHeight = min(
            max(finiteNonnegative(imageHeight), minImageSize.height),
            Self.maximumSafeDimension
        )
        let totalWidth = min(itemWidth * CGFloat(maxRating), Self.maximumSafeDimension)

        return CGSize(width: totalWidth, height: itemHeight)
    }

    public override func layoutSubviews() {
        super.layoutSubviews()

        guard let emptyImage else {
            setImageFrames(.zero)
            refresh()
            return
        }

        let imageCount = emptyImageViews.count
        guard imageCount > 0 else {
            return
        }

        let layoutWidth = finiteNonnegative(bounds.width, maximum: Self.maximumSafeDimension)
        let layoutHeight = finiteNonnegative(bounds.height, maximum: Self.maximumSafeDimension)
        guard layoutWidth > 0, layoutHeight > 0 else {
            setImageFrames(.zero)
            refresh()
            return
        }

        let desiredImageWidth = layoutWidth / CGFloat(imageCount)
        let maximumImageWidth = min(max(minImageSize.width, desiredImageWidth), layoutWidth)
        let maximumImageHeight = min(max(minImageSize.height, layoutHeight), layoutHeight)
        let imageViewSize = sizeForImage(
            emptyImage,
            inSize: CGSize(width: maximumImageWidth, height: maximumImageHeight)
        )
        let usedWidth = imageViewSize.width * CGFloat(imageCount)
        let imageXOffset = imageCount > 1
            ? (layoutWidth - usedWidth) / CGFloat(imageCount - 1)
            : 0

        for index in 0..<imageCount {
            let x = bounds.origin.x + CGFloat(index) * (imageXOffset + imageViewSize.width)
            let imageFrame = CGRect(
                x: finiteCoordinate(x, fallback: bounds.origin.x),
                y: finiteCoordinate(bounds.origin.y, fallback: 0),
                width: imageViewSize.width,
                height: imageViewSize.height
            )
            emptyImageViews[index].frame = imageFrame
            fullImageViews[index].frame = imageFrame
        }

        refresh()
    }

    func refresh() {
        guard emptyImage != nil, fullImage != nil else {
            fullImageViews.forEach {
                $0.layer.mask = nil
                $0.isHidden = true
            }
            updateAccessibilityState()
            return
        }

        for (index, imageView) in fullImageViews.enumerated() {
            if rating >= Float(index + 1) {
                imageView.layer.mask = nil
                imageView.isHidden = false
            } else if rating > Float(index), rating < Float(index + 1) {
                let fraction = finiteNonnegative(CGFloat(rating - Float(index)), maximum: 1)
                let maskWidth = finiteNonnegative(
                    fraction * finiteNonnegative(imageView.bounds.width, maximum: Self.maximumSafeDimension),
                    maximum: Self.maximumSafeDimension
                )
                let maskHeight = finiteNonnegative(
                    imageView.bounds.height,
                    maximum: Self.maximumSafeDimension
                )
                let maskLayer = CALayer()
                maskLayer.frame = CGRect(x: 0, y: 0, width: maskWidth, height: maskHeight)
                maskLayer.backgroundColor = UIColor.black.cgColor
                imageView.layer.mask = maskLayer
                imageView.isHidden = false
            } else {
                imageView.layer.mask = nil
                imageView.isHidden = true
            }
        }

        updateAccessibilityState()
    }

    func sizeForImage(_ image: UIImage, inSize size: CGSize) -> CGSize {
        let imageWidth = finiteNonnegative(image.size.width, maximum: Self.maximumSafeDimension)
        let imageHeight = finiteNonnegative(image.size.height, maximum: Self.maximumSafeDimension)
        let availableWidth = finiteNonnegative(size.width, maximum: Self.maximumSafeDimension)
        let availableHeight = finiteNonnegative(size.height, maximum: Self.maximumSafeDimension)

        guard imageWidth > 0, imageHeight > 0, availableWidth > 0, availableHeight > 0 else {
            return .zero
        }

        let scale = min(availableWidth / imageWidth, availableHeight / imageHeight)
        guard scale.isFinite, scale > 0 else {
            return .zero
        }

        return CGSize(
            width: min(imageWidth * scale, availableWidth),
            height: min(imageHeight * scale, availableHeight)
        )
    }

    func removeImageViews() {
        (emptyImageViews + fullImageViews).forEach { $0.removeFromSuperview() }
        emptyImageViews.removeAll(keepingCapacity: false)
        fullImageViews.removeAll(keepingCapacity: false)
    }

    func initImageViews() {
        guard emptyImageViews.isEmpty else {
            return
        }

        for _ in 0..<maxRating {
            let emptyImageView = makeImageView(image: emptyImage)
            emptyImageViews.append(emptyImageView)
            addSubview(emptyImageView)

            let fullImageView = makeImageView(image: fullImage)
            fullImageViews.append(fullImageView)
            addSubview(fullImageView)
        }
    }

    func handleTouchAtLocation(_ touchLocation: CGPoint) {
        guard editable, emptyImage != nil, fullImage != nil, !emptyImageViews.isEmpty else {
            return
        }

        var newRating: Float = 0
        for index in stride(from: emptyImageViews.count - 1, through: 0, by: -1) {
            let imageView = emptyImageViews[index]
            guard imageView.frame.width > 0 else {
                continue
            }

            if touchLocation.x > imageView.frame.origin.x {
                let newLocation = imageView.convert(touchLocation, from: self)
                if imageView.point(inside: newLocation, with: nil), floatRatings || halfRatings {
                    let decimal = Float(newLocation.x / imageView.frame.width)
                    newRating = Float(index) + decimal
                    if halfRatings {
                        newRating = Float(index) + (decimal > 0.75 ? 1 : (decimal > 0.25 ? 0.5 : 0))
                    }
                } else {
                    newRating = Float(index) + 1
                }
                break
            }
        }

        rating = boundedRating(newRating)
        delegate?.heartRatingView?(self, isUpdating: rating)
    }

    public override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard editable, let touch = touches.first else {
            return
        }
        handleTouchAtLocation(touch.location(in: self))
    }

    public override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard editable, let touch = touches.first else {
            return
        }
        handleTouchAtLocation(touch.location(in: self))
    }

    public override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {
        guard editable, !touches.isEmpty else {
            return
        }

        delegate?.heartRatingView(self, didUpdate: rating)
        bounceImageForCurrentRating()
    }

    public override func accessibilityIncrement() {
        adjustRatingForAccessibility(by: 1)
    }

    public override func accessibilityDecrement() {
        adjustRatingForAccessibility(by: -1)
    }

    private static let maximumSafeDimension = CGFloat(1_000_000)
    private static let maximumRatingCount = 100

    private func initializeControl() {
        isAccessibilityElement = true
        if accessibilityLabel == nil {
            accessibilityLabel = "Rating"
        }
        initImageViews()
        updateAccessibilityState()
    }

    private func makeImageView(image: UIImage?) -> UIImageView {
        let imageView = UIImageView(image: image)
        imageView.contentMode = imageContentMode
        imageView.isAccessibilityElement = false
        return imageView
    }

    private func setImageFrames(_ frame: CGRect) {
        emptyImageViews.forEach { $0.frame = frame }
        fullImageViews.forEach { $0.frame = frame }
    }

    private func boundedRating(_ candidate: Float) -> Float {
        guard candidate.isFinite else {
            return candidate.isNaN || candidate.sign == .minus ? Float(minRating) : Float(maxRating)
        }
        return min(max(candidate, Float(minRating)), Float(maxRating))
    }

    private func finiteNonnegative(_ value: CGFloat, maximum: CGFloat? = nil) -> CGFloat {
        guard value.isFinite, value >= 0 else {
            return 0
        }
        if let maximum {
            return min(value, maximum)
        }
        return value
    }

    private func finiteCoordinate(_ value: CGFloat, fallback: CGFloat) -> CGFloat {
        value.isFinite ? value : fallback
    }

    private func accessibilityRatingText() -> String {
        let ratingText = rating.rounded() == rating ? String(Int(rating)) : String(rating)
        return "\(ratingText) of \(maxRating)"
    }

    private func updateAccessibilityState() {
        accessibilityValue = accessibilityRatingText()
        accessibilityTraits = editable ? [.adjustable] : [.staticText]
    }

    private func adjustRatingForAccessibility(by delta: Float) {
        guard editable else {
            return
        }
        rating = boundedRating(rating + delta)
        delegate?.heartRatingView(self, didUpdate: rating)
        bounceImageForCurrentRating()
    }

    private func bounceImageForCurrentRating() {
        guard shouldBounce, !fullImageViews.isEmpty else {
            return
        }

        let rawIndex = Int(max(rating - 1, 0))
        let imageViewIndex = min(max(rawIndex, 0), fullImageViews.count - 1)
        fullImageViews[imageViewIndex].transform = CGAffineTransform(scaleX: 0.1, y: 0.1)

        UIView.animate(
            withDuration: 2,
            delay: 0,
            usingSpringWithDamping: 0.2,
            initialSpringVelocity: 9,
            options: [.allowUserInteraction],
            animations: { [weak self] in
                self?.fullImageViews[imageViewIndex].transform = .identity
            }
        )
    }
}
