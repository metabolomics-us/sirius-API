document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("compound-form");
    const output = document.getElementById("output");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        output.innerHTML = "Fetching results<span class='loading-dots'></span>";
        const msms = document.getElementById("msms-input").value.trim();
        const pcm = document.getElementById("pcm-input").value.trim();

        try {
            const response = await fetch("/compounds", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `msms_str=${encodeURIComponent(msms)}&pcm_str=${encodeURIComponent(pcm)}`
            });

            const result = await response.json();

            if (response.ok) {
                output.textContent = result.join("\n");
            } else {
                output.textContent = "Error: " + result.detail;
            }
        } catch (error) {
            output.textContent = "Network or server error occurred.";
            console.error(error);
        }
    });
});
