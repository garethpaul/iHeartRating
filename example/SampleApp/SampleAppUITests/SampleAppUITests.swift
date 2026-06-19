import XCTest

final class SampleAppUITests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testApplicationLaunches() {
        let application = XCUIApplication()
        application.launch()
        XCTAssertEqual(application.state, .runningForeground)
    }
}
