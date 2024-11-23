import UIKit

class ViewController: UIViewController {
    
    @IBOutlet weak var welcomeLabel: UILabel!
    @IBOutlet weak var descriptionLabel: UILabel!
    @IBOutlet weak var userCountLabel: UILabel!
    @IBOutlet weak var dateLabel: UILabel!
    @IBOutlet weak var actionButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        updateLocalizedContent()
    }
    
    private func updateLocalizedContent() {
        welcomeLabel.text = NSLocalizedString("welcome.title", comment: "Welcome message")
        descriptionLabel.text = NSLocalizedString("welcome.description", comment: "App description")
        
        let userCount = 1234
        userCountLabel.text = String(format: NSLocalizedString("users.count", comment: "User count"), NSNumber(value: userCount))
        
        let date = Date()
        let dateFormatter = DateFormatter()
        dateFormatter.dateStyle = .long
        let dateString = dateFormatter.string(from: date)
        dateLabel.text = String(format: NSLocalizedString("last.updated", comment: "Last updated date"), dateString as NSString)
        
        actionButton.setTitle(NSLocalizedString("action.button", comment: "Action button title"), for: .normal)
    }
}
