import Foundation
import AppKit

@objc public class LocalizationHelper: NSObject {
    
    // MARK: - Text Size Estimation
    @objc public static func estimateTextSize(_ text: String, font: NSFont, width: CGFloat) -> CGSize {
        let textField = NSTextField(wrappingLabelWithString: text)
        textField.font = font
        textField.preferredMaxLayoutWidth = width
        let size = textField.fittingSize
        return size
    }
    
    // MARK: - Layout Direction
    @objc public static func isRTL(forLanguage language: String) -> Bool {
        return language.hasPrefix("ar") || language.hasPrefix("he") || language.hasPrefix("fa")
    }
    
    // MARK: - Text Analysis
    @objc public static func analyzeText(_ text: String) -> [String: Any] {
        let lines = text.components(separatedBy: .newlines)
        let words = text.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }
        
        return [
            "length": text.count,
            "lines": lines.count,
            "words": words.count,
            "hasDirectionalOverrides": containsDirectionalOverrides(text),
            "formatSpecifiers": findFormatSpecifiers(text)
        ]
    }
    
    // MARK: - Specific Checks
    @objc public static func findFormatSpecifiers(_ text: String) -> [String] {
        let pattern = "%[0-9]*(@|d|f|s)"
        let regex = try? NSRegularExpression(pattern: pattern, options: [])
        let range = NSRange(location: 0, length: text.utf16.count)
        let matches = regex?.matches(in: text, options: [], range: range) ?? []
        
        return matches.map { match in
            if let range = Range(match.range, in: text) {
                return String(text[range])
            }
            return ""
        }
    }
    
    @objc public static func containsDirectionalOverrides(_ text: String) -> Bool {
        // Check for Unicode directional formatting characters
        let overrides = ["\u{202A}", "\u{202B}", "\u{202C}", "\u{202D}", "\u{202E}"]
        return overrides.contains { text.contains($0) }
    }
    
    // MARK: - Layout Testing
    @objc public static func simulateLayoutForLanguage(_ language: String, text: String, width: CGFloat) -> [String: Any] {
        let isRTL = isRTL(forLanguage: language)
        let font = NSFont.systemFont(ofSize: NSFont.systemFontSize)
        let size = estimateTextSize(text, font: font, width: width)
        
        return [
            "width": size.width,
            "height": size.height,
            "isRTL": isRTL,
            "recommendedMinWidth": ceil(size.width * 1.1), // 10% margin
            "textAnalysis": analyzeText(text)
        ]
    }
    
    // MARK: - Screen Metrics
    @objc public static func getScreenMetrics() -> [String: Any] {
        let screen = NSScreen.main
        return [
            "width": screen?.frame.width ?? 0,
            "height": screen?.frame.height ?? 0,
            "scale": screen?.backingScaleFactor ?? 1.0,
            "isRTL": NSApplication.shared.userInterfaceLayoutDirection == .rightToLeft
        ]
    }
    
    // MARK: - Validation
    @objc public static func validateTranslation(source: String, translated: String) -> [String: Any] {
        let sourceAnalysis = analyzeText(source)
        let translatedAnalysis = analyzeText(translated)
        let sourceSpecifiers = findFormatSpecifiers(source)
        let translatedSpecifiers = findFormatSpecifiers(translated)
        
        return [
            "lengthRatio": Double(translated.count) / Double(source.count),
            "specifiersMatch": sourceSpecifiers == translatedSpecifiers,
            "sourceSpecifiers": sourceSpecifiers,
            "translatedSpecifiers": translatedSpecifiers,
            "source": sourceAnalysis,
            "translated": translatedAnalysis,
            "recommendation": generateRecommendation(
                sourceLength: source.count,
                translatedLength: translated.count,
                sourceSpecifiers: sourceSpecifiers,
                translatedSpecifiers: translatedSpecifiers
            )
        ]
    }
    
    private static func generateRecommendation(
        sourceLength: Int,
        translatedLength: Int,
        sourceSpecifiers: [String],
        translatedSpecifiers: [String]
    ) -> String {
        var recommendations: [String] = []
        
        let ratio = Double(translatedLength) / Double(sourceLength)
        if ratio > 1.5 {
            recommendations.append("Translation is \(Int(ratio * 100))% longer than source - consider shortening")
        }
        
        if sourceSpecifiers != translatedSpecifiers {
            recommendations.append("Format specifiers don't match - please verify")
        }
        
        return recommendations.isEmpty ? "No issues found" : recommendations.joined(separator: "; ")
    }
}
