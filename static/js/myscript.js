
function todostatus(id){
    var c= document.getElementById('done_' + id);
    var status=c.checked ? "Completed" : "Incomplete";
    document.getElementById('todo_status_' + id).innerText=status;
}