window.addEventListener('DOMContentLoaded', function() {
    const appearBox = document.getElementById('appear-box');
    document.getElementById('twitter').addEventListener('click', function() {
        appearBox.style.visibility = 'visible';
        const myinput = document.getElementById('myinput');
        myinput.placeholder = 'Enter your Twitter Username';
        const myForm = document.getElementById('socialForm');
        myForm.action = '/twitter';
    });
    document.getElementById('youtube').addEventListener('click', function() {
        appearBox.style.visibility = 'visible';
        const myinput = document.getElementById('myinput');
        myinput.placeholder = 'Enter Youtube video url';
        const myForm = document.getElementById('socialForm');
        myForm.action = '/youtube';
    });
    document.getElementById('reddit').addEventListener('click', function() {
        appearBox.style.visibility = 'visible';
        const myinput = document.getElementById('myinput');
        myinput.placeholder = 'Enter your Reddit Post Url';
        const myForm = document.getElementById('socialForm');
        myForm.action = '/reddit';
    });
    document.getElementById('facebook').addEventListener('click', function() {
        appearBox.style.visibility = 'visible';
        const myinput = document.getElementById('myinput');
        myinput.placeholder = 'Enter your Facebook Username';
        const myForm = document.getElementById('socialForm');
        myForm.action = '/facebook';
    });
    document.getElementById('instagram').addEventListener('click', function() {
        appearBox.style.visibility = 'visible';
        const myinput = document.getElementById('myinput');
        myinput.placeholder = 'Enter your Instagram Username';
        const myForm = document.getElementById('socialForm');
        myForm.action = '/instagram';
    });
});
