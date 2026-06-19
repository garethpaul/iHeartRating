
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

        final class ViewController: UIViewController, HeartRatingViewDelegate {
            func heartRatingView(_ ratingView: HeartRatingView, isUpdating rating: Float) {
                // do something while (rating) has been initiated
            }

            func heartRatingView(_ ratingView: HeartRatingView, didUpdate rating: Float) {
                // do something when (rating) object has been updates
            }
        }

Step 4.
-------

Open up the Main.storyboard to view the main view controller.


----------


Hope this was useful to share.
