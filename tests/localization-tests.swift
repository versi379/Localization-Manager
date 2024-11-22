import XCTest
@testable import LocalizationQA

class LocalizationTests: XCTestCase {
    var localizationManager: CrossPlatformLocalizationManager!
    
    override func setUp() {
        super.setUp()
        localizationManager = CrossPlatformLocalizationManager.shared
    }
    
    // Language Switching Tests
    func testLanguageSwitching() {
        CrossPlatformLocalizationManager.SupportedLanguage.allCases.forEach { language in
            localizationManager.switchLanguage(to: language)
            
            // Verify localization key exists
            let localizedWelcome = NSLocalizedString("welcome_message", comment: "")
            XCTAssertFalse(localizedWelcome.isEmpty, "Localization failed for \(language)")
        }
    }
    
    // Text Overflow Detection Tests
    func testTextOverflowDetection() {
        let testView = UIView(frame: CGRect(x: 0, y: 0, width: 300, height: 200))
        let testLabel = UILabel(frame: CGRect(x: 0, y: 0, width: 200, height: 50))
        testLabel.text = NSLocalizedString("test_overflow_message", comment: "")
        testLabel.numberOfLines = 0
        testView.addSubview(testLabel)
        
        let overflowResults = localizationManager.detectTextOverflow(in: testView)
        XCTAssertFalse(overflowResults.isEmpty, "Overflow detection failed")
    }
    
    // RTL Layout Support Test
    func testRTLLayoutSupport() {
        localizationManager.switchLanguage(to: .arabic)
        
        #if os(iOS)
        let isRTL = UIApplication.shared.userInterfaceLayoutDirection == .rightToLeft
        XCTAssertTrue(isRTL, "RTL layout not configured for Arabic")
        #endif
    }
    
    // Comprehensive Localization Report Test
    func testLocalizationReport() {
        let testView = UIView(frame: CGRect(x: 0, y: 0, width: 300, height: 200))
        let report = localizationManager.generateLocalizationReport(for: testView)
        
        XCTAssertNotNil(report["textOverflows"], "Overflow report generation failed")
        XCTAssertNotNil(report["isRTLLayout"], "RTL layout detection failed")
        XCTAssertNotNil(report["supportedLanguages"], "Language support report failed")
    }
}
