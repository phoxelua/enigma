
        function fade(btnElement) {
            if (btnElement.value === "Fade Out") {
                document.getElementById("sphinx").className = "fade-out";
                btnElement.value = "Fade In";
            }
            else {
                document.getElementById("sphinx").className = "fade-in";
                btnElement.value = "Fade Out";
            }
        }
