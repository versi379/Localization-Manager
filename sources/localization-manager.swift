import Foundation
#if os(iOS)
import UIKit
#elseif os(macOS)
import AppKit
#endif

class LocalizationQAManager {
    static let shared = LocalizationQAManager()
    
    enum SupportedLanguage: String, CaseIterable {
        case english = "en"
        case arabic = "ar"
        case spanish = "es"
        case chinese = "zh-Hans"
    }
    
    #if os(iOS)
    typealias View = UIView
    typealias Label = UILabel
    typealias Font = UIFont
    #elseif os(macOS)
    typealias View = NSView
    typealias Label = NSTextField
    typealias Font = NSFont
    #endif
    
    func switchLanguage(to language: SupportedLanguage) {
        UserDefaults.standard.set([language.rawValue], forKey: "AppleLanguages")
        UserDefaults.standard.synchronize()
        
        // Platform-specific UI update notification
        #if os(iOS)
        NotificationCenter.default.post(name: NSNotification.Name("LanguageChanged"), object: nil)
        #elseif os(macOS)
        DistributedNotificationCenter.default().post(
            name: NSNotification.Name("LanguageChanged"), 
            object: nil
        )
        #endif
    }
    
    // [Rest of the implementation remains the same as in previous artifact]
}
