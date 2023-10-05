document.addEventListener("DOMContentLoaded", function() {
    var currentSlide = 0;
    var slides = document.getElementsByClassName("slide");
  
    function changeSlide() {
      // Fade out the current slide
      slides[currentSlide].classList.remove("active");
  
      // Move to the next slide
      currentSlide++;
      if (currentSlide >= slides.length) {
        currentSlide = 0;
      }
  
      // Fade in the next slide
      slides[currentSlide].classList.add("active");
    }
  
    // Set the first slide to active
    slides[currentSlide].classList.add("active");
  
    // Change the slide every 8 seconds
    setInterval(changeSlide, 8000);
  });  