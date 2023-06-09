<script src="https://cdn.jsdelivr.net/npm/brython@3/brython.min.js">
</script>
<script src="https://cdn.jsdelivr.net/npm/brython@3/brython_stdlib.js">
</script>
function performTraceroute() {
    var url = document.getElementById("url-input").value;
    
    // Make an AJAX request to the server with the entered URL
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        var response = xhr.responseText;
        eval(response); // Evaluate the Python code returned by the server
      }
    };
    xhr.open("POST", "/traceroute");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("url=" + encodeURIComponent(url));
  }
  