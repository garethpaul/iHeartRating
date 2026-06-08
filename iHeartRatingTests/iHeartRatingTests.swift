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

    func testZeroSizeImageReturnsZeroSize() {
        let hrv = HeartRatingView.init(frame: CGRect(x: 0, y: 0, width: 100, height: 20))
        let imageSize = hrv.sizeForImage(UIImage(), inSize: CGSizeZero)
        XCTAssert(imageSize.width == 0)
        XCTAssert(imageSize.height == 0)
    }
    
    func testPerformanceExample() {
        // This is an example of a performance test case.
        self.measureBlock {
            // Put the code you want to measure the time of here.
        }
    }
    
}
