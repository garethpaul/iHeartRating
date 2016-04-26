
## Sample App ##
----------
<img src="https://raw.githubusercontent.com/garethpaul/iHeartRating/master/screenshots/heart_app_example.gif" width="192" align="right">


This should get you going quick simply.

**Getting Started**
-------------------

Step 1.
-------
 Get the cocoapod

    pod install


Step 2.
-------

`open SampleApp.xcworkspace`

Step 3.
-------

Look at code in ViewController.swift

 - Note the HeartRatingViewDelegate
 - Two Ratings Functions to conform to the protocol.



      import UIKit
        import iHeartRating

        class ViewController: UIViewController, HeartRatingViewDelegate {

           override func viewDidLoad() {
                super.viewDidLoad()
                // Do any additional setup after loading the view, typically from a nib.
            }

            override func didReceiveMemoryWarning() {
                super.didReceiveMemoryWarning()
                // Dispose of any resources that can be recreated.
            }

            func heartRatingView(ratingView: HeartRatingView, isUpdating rating:Float) {
                // do something while (rating) has been initiated
            }

            func heartRatingView(ratingView: HeartRatingView, didUpdate rating: Float) {
                // do something when (rating) object has been updates
            }


        }

Step 4.
-------

Open up the Main.storyboard to view the main view controller.


----------


Hope this was useful to share.
