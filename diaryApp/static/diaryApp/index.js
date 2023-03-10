function expand_entry(id) {
    document.querySelector(`#${id}`).classList.toggle('expand');
}

function edit_entry(id) {

    if (document.querySelector(`#entry-${id}`).className === "diary-entries expand") {
        if (document.getElementById(`edit-text${id}`) === null) {
            const existing_content = document.querySelector(`#entry-body${id}`).textContent;
            document.querySelector(`#entry-body${id}`).innerHTML = 
            `<textarea class="edit-text" id="edit-text${id}">${existing_content.trim()}</textarea>

            <button class="btn btn-success" id="submit-edit">Submit</button>
            `
            const existing_date = document.querySelector(`#entry-date-${id}`).textContent;
            document.querySelector(`#entry-date-${id}`).innerHTML =`<textarea class="edit-date" id="date-${id}">${existing_date.trim()}</textarea>`
            

            document.querySelector("#submit-edit").addEventListener('click', () => {
                
                console.log(document.querySelector(`#date-${id}`).value)
        
                

                fetch(`edit_post/${id}`, {
                    method: 'PUT',
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        body: document.querySelector(`#edit-text${id}`).value,
                        date: document.querySelector(`#date-${id}`).value
                    })
                })
                .then(response => response.json())
                .then(entry => {
                    document.querySelector(`#entry-body${id}`).innerHTML = entry.body
                    document.querySelector(`#entry-date-${id}`).innerHTML = `
                    <label id="entry-date" onclick="expand_entry('entry-${id}')">&nbsp;&nbsp;&nbsp;&nbsp;${entry.date.trim()}</label>
                    `
                    document.querySelector(`#entry-weekday-${id}`).innerHTML = entry.weekday;

                })
            })

        }
    }
}



function save_task(ids) {
    fetch(`update_task/${ids}`, {
        method: 'PUT'
    }); 
}

function remove_task(ids) {
    entry_task = ids.split(",")
    task_id = entry_task[1]
    fetch(`remove/${ids}`, {
        method: 'PUT'
    })

    document.querySelector(`#grid-${task_id}`).remove()

}

function compose() {
    
    fetch(`compose`, {
        method: 'PUT'
    })
    setTimeout(function(){
        window.location.reload();
     }, 500);


}

function edit_task(ids) {

    entry_task = ids.split(",");

    task_id = entry_task[0];
    console.log(task_id)
    
    entry_id = entry_task[1];
    console.log(entry_id)
    
    const new_task_name = document.getElementById(`task-name-change${entry_id}${task_id}`).value;
    console.log(new_task_name)
    old_task = document.getElementById(`${task_id},${entry_id}`)
    console.log(old_task)
    if (new_task_name.length > 25) {
        alert("Cannot be over 25 characters long.")
        return;
    }
    fetch(`edit_task_name/${task_id}/${entry_id}/${new_task_name}`, {
        method: 'PUT',
    })
    .then(response => response.json())
    .then(task => {
        old_task.innerHTML = task.task
    })
}

function add_task(entry_id) {



    const task_name = document.getElementById(`add-new-task${entry_id}`).value;
    if (task_name.length > 25) {
        alert("Cannot be over 25 characters long.")
        return;
    }
    fetch(`add_task/${entry_id}/${task_name}`, {
        method: 'PUT',
    })
    .then(response => response.json())
    .then(entry_task => {
        new_task = document.createElement('div')
        new_task.innerHTML = `
            <div class="grid-item">
                <input name="${ entry_task[0].id },${ entry_task[1].id }" onclick="save_task(this.name)" class="form-check-input" type="checkbox" id="flexSwitchCheckDefault">
                <label id="${ entry_task[1].id }" class="form-check-label" for="flexSwitchCheckDefault">${ entry_task[1].task }</label>
                <a href="#exampleModalCentre${ entry_task[1].id }" data-target="#exampleModalCenter${ entry_task[1].id }" role="button" data-toggle="modal"><img  id="edit-task" src="https://icons.veryicon.com/png/o/miscellaneous/linear-small-icon/edit-246.png" height="40px" width="40px" alt=""></a>
                <img id="remove-task" src="https://cdn3.iconfinder.com/data/icons/softwaredemo/PNG/256x256/DeleteRed.png" width="40px" height="40px" alt="">
            </div>
                <!-- Modal -->
            <div class="modal fade" id="exampleModalCenter${ entry_task[1].id }" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalCenterTitle">Change task name:</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                    </div>
                    <div class="modal-body">
                    <input type="text" id="task-name-change${ entry_task[1].id }">
                    </div>
                    <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    <button onclick="edit_task('${ entry_task[0].id },${entry_task[1].id }')" type="button" class="btn btn-primary">Save changes</button>
                    </div>
                </div>
                </div>
            </div>
        `
        document.querySelector(`#grid-${entry_task[0].id}`).append(new_task);
    })
}

function delete_entry(entry_id) {
    fetch(`delete_entry/${entry_id}`, {
        method: 'PUT'
    })
    .then(response => response.json())
    setTimeout(function(){
        location.reload();
     }, 500);
}



function change_date(date) {
    document.querySelector("#entry-date").innerHTML = `<input id="entry-date" value="${date}">
    <button class="btn btn-success" onclick="create_entry()">Save</button>
    `;  
}

function empty_content(content) {
    content.innerHTML = "";
}
       
    


   
