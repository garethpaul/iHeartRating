[![Build Status](https://travis-ci.org/garethpaul/iHeartRating.svg?branch=master)](https://travis-ci.org/garethpaul/iHeartRating)

<img src="https://raw.github.com/garethpaul/iheartrating/master/assets/logo.png" width="90" alt="Logo" style="display:block; width:90px;" />

# iHeartRating
Simple Ratings View for iOS enabling you to use any image as a rating e.g. hearts, stars, pigeons etc. We extend UIView to make it very easy to add ratings to your app

<img src="https://raw.githubusercontent.com/garethpaul/iHeartRating/master/screenshots/heart_app_example.gif" width="192">

# Getting Started
You want to add `pod 'iHeartRating', '~> 0.1'` to your Podfile:

```
target 'MyApp' do
  pod 'iHeartRating', '~> 0.1'
end
```

## Sample Usage

Here is a sample ViewController :-

```
import iHeartRating
class ViewController: UIViewController, HeartRatingViewDelegate {

  override func viewDidLoad() {
        super.viewDidLoad()
  }


  func heartRatingView(ratingView: HeartRatingView, isUpdating rating:Float) {
      // do something while (rating) has been initiated
  }

  func heartRatingView(ratingView: HeartRatingView, didUpdate rating: Float) {
      // do something when (rating) object has been updates
  }

}
```

In addition here is a sample setup in a storyboard

<img src="https://raw.github.com/garethpaul/iheartrating/master/assets/storyboard.png" alt="storyboard" style="width:150px" />
