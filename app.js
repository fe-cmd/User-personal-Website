const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');


menu.addEventListener('click', function() {
    menu.classList.toggle('is-active');
    menuLinks.classList.toggle('active');

});

const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.invalid_feedback');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');
const passwordField = document.querySelector('#passwordField');
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
const showPasswordToggle = document.querySelector('.showPasswordToggle');
const submitBtn = document.querySelector('.submit-btn');
const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === 'SHOW') {
    showPasswordToggle.textContent = 'HIDE';
    passwordField.setAttribute('type', 'text');
  } else {
    showPasswordToggle.textContent === 'SHOW';
    passwordField.setAttribute('type', 'password');
  }
};

showPasswordToggle.addEventListener('click', handleToggleInput);

emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove('is-invalid');
  emailFeedBackArea.style.display = 'none';

  if (emailVal.length > 0) {
    fetch('/authentication/validate-email', {
      body: JSON.stringify({email: emailVal }),
      method: 'POST',
    })

      .then((res) => res.json())
      .then((data) => {
        console.log('data', data);
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField.classList.add('is-invalid');
          emailFeedBackArea.style.display = 'block';
          emailFeedBackArea.innerHTML = '<p>$(data.email_error)</p>';
        }else{
          submitBtn.removeAttribute('disabled');
        }
      });
  }

});

usernameField.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;
  
  usernameSuccessOutput.style.display = 'block';

  usernameSuccessOutput.textContent = 'Checking ${usernameVal}';

  usernameField.classList.remove('is-invalid');
  usernameFeedBackArea.style.display = 'none';

  if (usernameVal.length > 0) {
    fetch('/authentication/validate-username', {
      body: JSON.stringify({username: usernameVal }),
      method: 'POST',
    })

      .then((res) => res.json())
      .then((data) => {
        console.log('data', data);
        usernameSuccessOutput.style.display = 'none';
        if (data.username_error) {
          submitBtn.disabled = true;
          usernameField.classList.add('is-invalid');
          feedBackArea.style.display = 'block';
          feedBackArea.innerHTML = '<p>$(data.username_error)</p>';
        }else{
          submitBtn.removeAttribute('disabled');
        }
      });
  }

});


var slideIndex = 1;
showSlides(slideIndex);
 +  
function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
}

// Open the Modal
function openModal() {
  document.getElementById("myModal").style.display = "block";
}

// Close the Modal
function closeModal() {
  document.getElementById("myModal").style.display = "none";
}

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  var captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}
