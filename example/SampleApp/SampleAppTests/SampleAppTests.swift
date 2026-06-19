import XCTest
@testable import SampleApp

final class SampleAppTests: XCTestCase {
    func testViewControllerLoads() {
        XCTAssertNotNil(ViewController().view)
    }
}
