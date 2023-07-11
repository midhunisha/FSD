const inputbox = document.getElementById("input-box");
const list = document.getElementById("list");
function addTask(){
    if(inputbox.value === ''){
        alert("Empty task cannot be added! Write something!");
    }
    else{
        let li = document.createElement("li");
        li.innerHTML = inputbox.value;
        list.appendChild(li);
        let span = document.createElement("span");
        span.innerHTML = "X";
        li.appendChild(span)
    }
    inputbox.value = "";
    saveData();
}
list.addEventListener("click", function(e)
{
    if(e.target.tagName === "LI")
    {
        e.target.classList.toggle("done");
        saveData();
    }
    else if(e.target.tagName === "SPAN")
    {
        e.target.parentElement.remove();
        saveData();
    }
},false);
 function saveData(){
    localStorage.setItem("data", list.innerHTML);
}
function showTask(){
    list.innerHTML = localstorage.getItem("data");
}
showTask();