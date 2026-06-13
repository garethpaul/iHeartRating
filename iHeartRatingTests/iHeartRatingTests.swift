//
//  iHeartRatingTests.swift
//  iHeartRatingTests
//
//  Created by Gareth on 7/1/16.
//  Copyright © 2016 GPJ. All rights reserved.
//

import XCTest
import UIKit

@testable import iHeartRating

class RecordingHeartRatingDelegate: NSObject, HeartRatingViewDelegate {
    var didUpdateCount = 0
    var isUpdatingCount = 0

    func heartRatingView(ratingView: HeartRatingView, didUpdate rating: Float) {
        didUpdateCount += 1
    }

    func heartRatingView(ratingView: HeartRatingView, isUpdating rating: Float) {
        isUpdatingCount += 1
    }
}

class iHeartRatingTests: XCTestCase {
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testExample() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 1000, height: 1000))
        XCTAssert(hrv.frame.height == 1000)
        
    }

    func testMaxRatingDoesNotStayBelowOne() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.maxRating = 0
        XCTAssert(hrv.maxRating == 1)
    }

    func testRatingDoesNotExceedMaxRating() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.maxRating = 3
        hrv.rating = 9
        XCTAssert(hrv.rating == 3)
    }

    func testNaNRatingFallsBackToMinRating() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.minRating = 2
        hrv.rating = Float(0.0) / Float(0.0)
        XCTAssert(hrv.rating == 2)
    }

    func testMinRatingDoesNotExceedMaxRating() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.maxRating = 2
        hrv.minRating = 5
        XCTAssert(hrv.minRating == 2)
        XCTAssert(hrv.rating == 2)
    }

    func testZeroSizeImageReturnsZeroSize() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let imageSize = hrv.sizeForImage(UIImage(), inSize: CGSizeZero)
        XCTAssert(imageSize.width == 0)
        XCTAssert(imageSize.height == 0)
    }

    func testMinImageSizeDoesNotStayNegative() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.minImageSize = CGSize(width: -10, height: -5)
        XCTAssert(hrv.minImageSize.width == 0)
        XCTAssert(hrv.minImageSize.height == 0)
    }

    func testMinImageSizeDoesNotStayNaN() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let nan = CGFloat(Float(0.0) / Float(0.0))

        hrv.minImageSize = CGSize(width: nan, height: 12)
        XCTAssert(hrv.minImageSize.width == 0)
        XCTAssert(hrv.minImageSize.height == 12)

        hrv.minImageSize = CGSize(width: 15, height: nan)
        XCTAssert(hrv.minImageSize.width == 15)
        XCTAssert(hrv.minImageSize.height == 0)
    }

    func testLayoutUsesLocalBoundsWhenViewIsScaled() {
        UIGraphicsBeginImageContextWithOptions(CGSize(width: 20, height: 20), false, 1)
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()

        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.emptyImage = image
        hrv.transform = CGAffineTransformMakeScale(2, 2)
        hrv.layoutSubviews()

        let firstImageView = hrv.subviews.first as! UIImageView
        XCTAssert(hrv.frame.size.width == 200)
        XCTAssert(hrv.bounds.size.width == 100)
        XCTAssert(abs(firstImageView.frame.size.width - 20) < 0.001)
    }

    func testIncompleteImagePairHidesAndRestoresFullImages() {
        UIGraphicsBeginImageContextWithOptions(CGSize(width: 20, height: 20), false, 1)
        let image = UIGraphicsGetImageFromCurrentImageContext()
        UIGraphicsEndImageContext()

        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        hrv.emptyImage = image
        hrv.fullImage = image
        hrv.rating = 0.5
        hrv.layoutSubviews()

        let firstFullImageView = hrv.subviews[1] as! UIImageView
        XCTAssertFalse(firstFullImageView.hidden)
        XCTAssertNotNil(firstFullImageView.layer.mask)

        hrv.emptyImage = nil
        XCTAssertTrue(firstFullImageView.hidden)
        XCTAssertNil(firstFullImageView.layer.mask)

        hrv.emptyImage = image
        hrv.layoutSubviews()
        XCTAssertFalse(firstFullImageView.hidden)
        XCTAssertNotNil(firstFullImageView.layer.mask)
    }

    func testTouchesEndedDoesNotNotifyWhenNotEditable() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let delegate = RecordingHeartRatingDelegate()
        hrv.delegate = delegate
        hrv.editable = false

        hrv.touchesEnded(Set<UITouch>(), withEvent: nil)

        XCTAssert(delegate.didUpdateCount == 0)
    }

    func testTouchesEndedDoesNotNotifyWithoutTouches() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let delegate = RecordingHeartRatingDelegate()
        hrv.delegate = delegate

        hrv.touchesEnded(Set<UITouch>(), withEvent: nil)

        XCTAssert(delegate.didUpdateCount == 0)
    }

    func testTouchesBeganDoesNotNotifyWithoutTouches() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let delegate = RecordingHeartRatingDelegate()
        hrv.delegate = delegate

        hrv.touchesBegan(Set<UITouch>(), withEvent: nil)

        XCTAssert(delegate.isUpdatingCount == 0)
    }

    func testTouchesMovedDoesNotNotifyWithoutTouches() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let delegate = RecordingHeartRatingDelegate()
        hrv.delegate = delegate

        hrv.touchesMoved(Set<UITouch>(), withEvent: nil)

        XCTAssert(delegate.isUpdatingCount == 0)
    }
    
    func testPerformanceExample() {
        // This is an example of a performance test case.
        self.measureBlock {
            // Put the code you want to measure the time of here.
        }
    }
    
}
