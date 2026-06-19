import XCTest
import UIKit

@testable import iHeartRating

final class RecordingHeartRatingDelegate: NSObject, HeartRatingViewDelegate {
    var didUpdateRatings: [Float] = []
    var updatingRatings: [Float] = []

    func heartRatingView(_ ratingView: HeartRatingView, didUpdate rating: Float) {
        didUpdateRatings.append(rating)
    }

    func heartRatingView(_ ratingView: HeartRatingView, isUpdating rating: Float) {
        updatingRatings.append(rating)
    }
}

final class iHeartRatingTests: XCTestCase {
    private func image(width: CGFloat = 20, height: CGFloat = 10) -> UIImage {
        let renderer = UIGraphicsImageRenderer(size: CGSize(width: width, height: height))
        return renderer.image { context in
            UIColor.black.setFill()
            context.fill(CGRect(x: 0, y: 0, width: width, height: height))
        }
    }

    private func configuredView(frame: CGRect = CGRect(x: 0, y: 0, width: 100, height: 20)) -> HeartRatingView {
        let view = HeartRatingView(frame: frame)
        let ratingImage = image()
        view.emptyImage = ratingImage
        view.fullImage = ratingImage
        return view
    }

    private func assertFinite(_ rect: CGRect, file: StaticString = #filePath, line: UInt = #line) {
        XCTAssertTrue(rect.origin.x.isFinite, file: file, line: line)
        XCTAssertTrue(rect.origin.y.isFinite, file: file, line: line)
        XCTAssertTrue(rect.size.width.isFinite, file: file, line: line)
        XCTAssertTrue(rect.size.height.isFinite, file: file, line: line)
        XCTAssertGreaterThanOrEqual(rect.size.width, 0, file: file, line: line)
        XCTAssertGreaterThanOrEqual(rect.size.height, 0, file: file, line: line)
    }

    func testRatingAndBoundsNormalizeInvalidValues() {
        let view = HeartRatingView(frame: .zero)
        view.maxRating = 0
        XCTAssertEqual(view.maxRating, 1)

        view.maxRating = 3
        view.minRating = 5
        XCTAssertEqual(view.minRating, 3)
        XCTAssertEqual(view.rating, 3)

        view.minRating = 2
        view.rating = .nan
        XCTAssertEqual(view.rating, 2)
        view.rating = .infinity
        XCTAssertEqual(view.rating, 3)
        view.rating = -.infinity
        XCTAssertEqual(view.rating, 2)
    }

    func testMaximumRatingCountIsBoundedBeforeAllocatingImageViews() {
        let view = HeartRatingView(frame: .zero)

        view.maxRating = 101

        XCTAssertEqual(view.maxRating, 100)
        XCTAssertEqual(view.subviews.count, 200)
    }

    func testMinimumImageSizeNormalizesEachInvalidDimension() {
        let view = HeartRatingView(frame: .zero)
        let invalidValues: [CGFloat] = [-1, .nan, .infinity, -.infinity]

        for invalidValue in invalidValues {
            view.minImageSize = CGSize(width: invalidValue, height: 12)
            XCTAssertEqual(view.minImageSize.width, 0)
            XCTAssertEqual(view.minImageSize.height, 12)

            view.minImageSize = CGSize(width: 15, height: invalidValue)
            XCTAssertEqual(view.minImageSize.width, 15)
            XCTAssertEqual(view.minImageSize.height, 0)
        }
    }

    func testSizeForImageRejectsNonFiniteAndNonPositiveContainers() {
        let view = HeartRatingView(frame: .zero)
        let ratingImage = image()
        let hostileSizes = [
            CGSize(width: CGFloat.nan, height: 10),
            CGSize(width: 10, height: CGFloat.infinity),
            CGSize(width: -CGFloat.infinity, height: 10),
            CGSize(width: -1, height: 10),
            .zero
        ]

        for hostileSize in hostileSizes {
            XCTAssertEqual(view.sizeForImage(ratingImage, inSize: hostileSize), .zero)
        }
    }

    func testExtremeMinimumImageSizeStillProducesFiniteBoundedFrames() {
        let view = configuredView()
        view.minImageSize = CGSize(
            width: CGFloat.greatestFiniteMagnitude,
            height: CGFloat.greatestFiniteMagnitude
        )

        view.layoutIfNeeded()

        XCTAssertEqual(view.subviews.count, 10)
        for subview in view.subviews {
            assertFinite(subview.frame)
            XCTAssertLessThanOrEqual(subview.frame.width, view.bounds.width)
            XCTAssertLessThanOrEqual(subview.frame.height, view.bounds.height)
        }
    }

    func testRepeatedLayoutKeepsPartialMaskFiniteAndStable() {
        let view = configuredView()
        view.rating = 0.5

        view.layoutIfNeeded()
        let fullImageView = view.subviews[1] as! UIImageView
        let firstMaskFrame = try! XCTUnwrap(fullImageView.layer.mask?.frame)
        assertFinite(firstMaskFrame)

        view.setNeedsLayout()
        view.layoutIfNeeded()
        let secondMaskFrame = try! XCTUnwrap(fullImageView.layer.mask?.frame)

        XCTAssertEqual(secondMaskFrame, firstMaskFrame)
        assertFinite(secondMaskFrame)
    }

    func testLayoutUsesLocalBoundsWhenViewIsScaled() {
        let view = configuredView()
        view.transform = CGAffineTransform(scaleX: 2, y: 2)

        view.layoutIfNeeded()

        let firstImageView = view.subviews.first as! UIImageView
        XCTAssertEqual(view.frame.width, 200, accuracy: 0.001)
        XCTAssertEqual(view.bounds.width, 100, accuracy: 0.001)
        XCTAssertEqual(firstImageView.frame.width, 20, accuracy: 0.001)
    }

    func testIntrinsicContentSizeTracksImagesCountAndMinimumSize() {
        let view = HeartRatingView(frame: .zero)
        view.emptyImage = image(width: 20, height: 10)
        view.fullImage = image(width: 24, height: 12)
        view.maxRating = 4
        view.minImageSize = CGSize(width: 30, height: 16)

        XCTAssertEqual(view.intrinsicContentSize.width, 120, accuracy: 0.001)
        XCTAssertEqual(view.intrinsicContentSize.height, 16, accuracy: 0.001)

        let container = UIView(frame: .zero)
        view.translatesAutoresizingMaskIntoConstraints = false
        container.addSubview(view)
        NSLayoutConstraint.activate([
            view.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            view.topAnchor.constraint(equalTo: container.topAnchor),
            view.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            view.bottomAnchor.constraint(equalTo: container.bottomAnchor)
        ])
        XCTAssertEqual(
            container.systemLayoutSizeFitting(UIView.layoutFittingCompressedSize),
            view.intrinsicContentSize
        )
    }

    func testIncompleteImagePairHasNoIntrinsicSizeAndHidesOverlays() {
        let view = configuredView()
        view.rating = 0.5
        view.layoutIfNeeded()
        let fullImageView = view.subviews[1] as! UIImageView
        XCTAssertFalse(fullImageView.isHidden)
        XCTAssertNotNil(fullImageView.layer.mask)

        view.emptyImage = nil

        XCTAssertEqual(view.intrinsicContentSize, .zero)
        XCTAssertTrue(fullImageView.isHidden)
        XCTAssertNil(fullImageView.layer.mask)
    }

    func testImageContentModePropagatesAndSurvivesImageViewReplacement() {
        let view = HeartRatingView(frame: .zero)
        view.imageContentMode = .scaleAspectFill
        view.maxRating = 3

        XCTAssertEqual(view.subviews.count, 6)
        for subview in view.subviews {
            XCTAssertEqual((subview as! UIImageView).contentMode, .scaleAspectFill)
        }

        XCTAssertTrue(view.responds(to: NSSelectorFromString("setImageContentMode:")))
    }

    func testAccessibilityStateTracksRatingAndEditability() {
        let view = configuredView()
        view.maxRating = 5
        view.rating = 2.5

        XCTAssertTrue(view.isAccessibilityElement)
        XCTAssertEqual(view.accessibilityLabel, "Rating")
        XCTAssertEqual(view.accessibilityValue, "2.5 of 5")
        XCTAssertTrue(view.accessibilityTraits.contains(.adjustable))

        view.editable = false

        XCTAssertFalse(view.accessibilityTraits.contains(.adjustable))
        XCTAssertTrue(view.accessibilityTraits.contains(.staticText))
    }

    func testAccessibilityAdjustmentsAreBoundedAndNotifyDelegate() {
        let view = configuredView()
        let delegate = RecordingHeartRatingDelegate()
        view.delegate = delegate
        view.maxRating = 2
        view.rating = 1

        view.accessibilityIncrement()
        view.accessibilityIncrement()
        view.accessibilityDecrement()

        XCTAssertEqual(view.rating, 1)
        XCTAssertEqual(delegate.didUpdateRatings, [2, 2, 1])
        XCTAssertEqual(view.accessibilityValue, "1 of 2")
    }

    func testEmptyAndNoneditableTouchesDoNotNotify() {
        let view = HeartRatingView(frame: .zero)
        let delegate = RecordingHeartRatingDelegate()
        view.delegate = delegate

        view.touchesBegan([], with: nil)
        view.touchesMoved([], with: nil)
        view.touchesEnded([], with: nil)
        view.editable = false
        view.touchesEnded([], with: nil)

        XCTAssertTrue(delegate.updatingRatings.isEmpty)
        XCTAssertTrue(delegate.didUpdateRatings.isEmpty)
    }
}
