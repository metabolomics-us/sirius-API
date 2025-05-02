document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("input-form");
    const output = document.getElementById("output");
    const submitButton = form.querySelector("button[type='submit']");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // disable submit button while processing query
        submitButton.disabled = true;
        const originalText = submitButton.textContent;
        submitButton.textContent = "Wait...";

        output.innerHTML = "Fetching results<span class='loading-dots'></span>";
        const msms = document.getElementById("msms-input").value.trim();
        const pcm = document.getElementById("pcm-input").value.trim();
        const chargeValue = document.querySelector('input[name="charge"]:checked').value;

        try {
            const response = await fetch("/formulas", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    msms_str: msms,
                    pcm_str: pcm,
                    charge: chargeValue
                })
            });

            const result = await response.json();

            if (response.ok) {
                let outputText = '';
                if (result.formulas.length == 0) {
                    outputText = "Sirius could not find any matching formulas.";
                } else {
                    outputText += "Formula".padEnd(15) + "Score".padEnd(9) + "Adduct".padEnd(12) + "Precursor Formula\n"; // header
                    for (let i = 0; i < result.formulas.length; i++) {
                        const formula = result.formulas[i].padEnd(15);
                        const score = String(result.sirius_scores[i]).padEnd(9);
                        const adduct = result.adducts[i].padEnd(12);
                        const precursor_formula = result.precursor_formulas[i];
                        outputText += formula + score + adduct + precursor_formula + '\n';
                    }
                }
                output.textContent = outputText;
            } else {
                output.textContent = "Error: " + (result.detail || JSON.stringify(result));
            }
        } catch (error) {
            output.textContent = "Network or server error occurred.";
            console.error(error);
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalText;
        }
    });
});
