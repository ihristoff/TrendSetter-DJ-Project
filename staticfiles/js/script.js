document.getElementById("profileBtn").addEventListener("click", function () {
    var dropdownMenu = document.getElementById("dropdownMenu");
    if (dropdownMenu.style.display === "none" || dropdownMenu.style.display === "") {
        dropdownMenu.style.display = "block";
    } else {
        dropdownMenu.style.display = "none";
    }
});

// Close the dropdown menu when clicking outside of it
window.onclick = function (event) {
    if (!event.target.matches('.profile-img')) {
        var dropdowns = document.getElementsByClassName("dropdown-menu");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.style.display === "block") {
                openDropdown.style.display = "none";
            }
        }
    }
}

//--------- animation counter ----------


document.addEventListener('DOMContentLoaded', function () {
    const counter = document.querySelector('.counter');
    const number = counter.querySelector('.number');
    const targetCount = parseInt(number.getAttribute('data-count'));
    let currentCount = 0;

    const updateCount = () => {
        if (currentCount < targetCount) {
            currentCount++;
            number.textContent = currentCount;
            setTimeout(updateCount, 20); // Adjust the timeout for faster or slower animation
        } else {
            number.textContent = targetCount;
        }
    };

    updateCount();
});


//
//
// var modal = document.getElementById("myModal");
//
// // Get the image and insert it inside the modal - use its "alt" text as a caption
// var img = document.getElementById("myImg");
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
// img.onclick = function(){
//   modal.style.display = "block";
//   modalImg.src = this.src;
//   captionText.innerHTML = this.alt;
// }
//
// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];
//
// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//   modal.style.display = "none";
// }
//




document.addEventListener('DOMContentLoaded', function () {
    const ratingButtons = document.querySelectorAll('#ratingForm .rate-button');
    const ratingInput = document.getElementById('ratingInput');

    ratingButtons.forEach(button => {
        button.addEventListener('click', function () {
            const ratingValue = this.getAttribute('data-rate');
            ratingInput.value = ratingValue;
            document.getElementById('formTypeInput').value = 'rating';
            document.getElementById('ratingForm').submit();
        });

        button.addEventListener('mouseover', function () {
            const ratingValue = this.getAttribute('data-rate');
            ratingButtons.forEach(btn => {
                if (btn.getAttribute('data-rate') <= ratingValue) {
                    btn.style.color = 'orange';
                } else {
                    btn.style.color = '#aaa';
                }
            });
        });

        button.addEventListener('mouseout', function () {
            ratingButtons.forEach(btn => {
                btn.style.color = '#aaa';
            });
        });
    });
});