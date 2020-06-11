document.getElementById("J_searchInput").value ="1";
var e = document.createEvent("MouseEvents");
e.initEvent("click", true, true);
document.getElementById("J_searchResultBtn").dispatchEvent(e);


document.getElementById("J_searchInput").value ="2";document.getElementById("J_searchResultBtn").click();

window.document.__webdriver_script_fn = (function () {
    document.getElementById("J_searchInput").value = "2";
    document.getElementById("J_searchResultBtn").click();
})();