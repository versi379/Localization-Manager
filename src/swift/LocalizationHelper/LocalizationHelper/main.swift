import Foundation

// Handle command line arguments
let args = CommandLine.arguments

guard args.count >= 2 else {
    print("Usage: LocalizationHelper <command> [arguments...]")
    exit(1)
}

let command = args[1]

switch command {
case "analyze":
    guard args.count >= 4 else {
        print("Usage: LocalizationHelper analyze <text> <width>")
        exit(1)
    }
    let text = args[2]
    let width = Double(args[3]) ?? 375.0
    
    let analysis = LocalizationHelper.analyzeText(text)
    let jsonData = try JSONSerialization.data(withJSONObject: analysis, options: .prettyPrinted)
    if let jsonString = String(data: jsonData, encoding: .utf8) {
        print(jsonString)
    }

case "validate":
    guard args.count >= 4 else {
        print("Usage: LocalizationHelper validate <source> <translation>")
        exit(1)
    }
    let source = args[2]
    let translation = args[3]
    
    let validation = LocalizationHelper.validateTranslation(source: source, translated: translation)
    let jsonData = try JSONSerialization.data(withJSONObject: validation, options: .prettyPrinted)
    if let jsonString = String(data: jsonData, encoding: .utf8) {
        print(jsonString)
    }

case "layout":
    guard args.count >= 4 else {
        print("Usage: LocalizationHelper layout <language> <text>")
        exit(1)
    }
    let language = args[2]
    let text = args[3]
    
    let layout = LocalizationHelper.simulateLayoutForLanguage(language, text: text, width: 375)
    let jsonData = try JSONSerialization.data(withJSONObject: layout, options: .prettyPrinted)
    if let jsonString = String(data: jsonData, encoding: .utf8) {
        print(jsonString)
    }

default:
    print("Unknown command: \(command)")
    exit(1)
}
