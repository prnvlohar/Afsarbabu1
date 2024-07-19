
// Get the search input and results elements
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("results");

// Hide the results when the search field loses focus
searchInput.addEventListener("blur", (event) => {
    // Add a timeout to avoid immediate hiding when clicking on a result
    setTimeout(() => {
        searchResults.style.display = "none";
    }, 200); // Adjust timing as needed
});

// Show the results when the search field is focused
searchInput.addEventListener("focus", (event) => {
    searchResults.style.display = "block";
});





function handleSearch() {
    const input = document.getElementById("searchInput").value.trim();
    const resultsDiv = document.getElementById("results");

    if (input.length === 0) {
        resultsDiv.style.display = "none";
        resultsDiv.innerHTML = "";
        return;
    }

    // Simulated AJAX call to get results for two sections: Ytopic and Assessment
    fetch(searchApiUrl + "?query=" + encodeURIComponent(input))
        .then(response => response.json())
        .then(data => {
            resultsDiv.innerHTML = "";
            resultsDiv.style.display = "block";

            // Section for Ytopic
            if (data.results.topic && data.results.topic.length > 0) {
                const topicSection = document.createElement("div");
                topicSection.innerHTML = "<h3>Topic</h3>";
                data.results.topic.forEach(item => {
                    const anchor = document.createElement("a");
                    anchor.href = "#";
                    anchor.className = "topic-link";
                    const div = document.createElement("div");
                    div.className = "result-item";
                    div.innerHTML = item.name;
                    anchor.appendChild(div);
                    topicSection.appendChild(anchor);
                });
                resultsDiv.appendChild(topicSection);
            }

            // Section for Assessment
            if (data.results.assessment && data.results.assessment.length > 0) {
                const assessmentSection = document.createElement("div");
                assessmentSection.innerHTML = "<h3>Assessment</h3>";
                data.results.assessment.forEach(item => {
                    const anchor = document.createElement("a");
                    anchor.href = "#";
                    anchor.className = "assessment-link";
                    const div = document.createElement("div");
                    div.className = "result-item";
                    div.innerHTML = "<span>" +
                        "<p style='display:inline;margin:0;'>" + item.name + "</p>" + "  " +
                        "<p style='display:inline;margin:0;opacity:0.5;'>" + item.subtopic + "</p>" +
                        "</span>";
                    anchor.appendChild(div);
                    assessmentSection.appendChild(anchor);
                });
                resultsDiv.appendChild(assessmentSection);
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            resultsDiv.innerHTML = "<div class='result-item'>An error occurred. Please try again later.</div>";
        });
}