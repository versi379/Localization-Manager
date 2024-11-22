import XCTest
#if os(iOS)
import UIKit
#elseif os(macOS)
import AppKit
#endif

class LocalizationQATestSuite: XCTestCase {
    func testLanguageSwitching() {
        let manager = LocalizationQAManager.shared
        
        LocalizationQAManager.SupportedLanguage.allCases.forEach { language in
            manager.switchLanguage(to: language)
            
            // Validate localization
            XCTAssertNotNil(Bundle.main.localizedString(forKey: "test_key", value: nil, table: nil))
        }
    }
    
    func testPlatformSpecificLocalization() {
        let manager = LocalizationQAManager.shared
        
        #if os(iOS)
        let viewController = UIViewController()
        let report = manager.generateLocalizationReport(for: viewController.view)
        XCTAssertNotNil(report["textOverflows"])
        #elseif os(macOS)
        let nsView = NSView()
        let report = manager.generateLocalizationReport(for: nsView)
        XCTAssertNotNil(report["supportedLanguages"])
        #endif
    }
}
