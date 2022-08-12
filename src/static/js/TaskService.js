
let TaskService = {

    // TODO: Put this in a separate utill.js file to re-use this func
    escapeInput(input) {
        return input.toString()
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;")
             .replace(/^\s+|\s+$/g,''); // trim
     },

    // TODO: Put this in a separate utill.js file to re-use this func
    getCookie(cookieName) {
      let name = cookieName + "=";
      let decodedCookie = decodeURIComponent(document.cookie);
      let ca = decodedCookie.split(';');
      for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    },

    // TODO: Put this in a separate utill.js file to re-use this func
    isUserLoggedIn() {
        // let temp_token = AuthService.getCookie('temp_token');
        let temp_token = TaskService.getCookie('temp_token');
        if (temp_token !== undefined && temp_token !== null && temp_token !== '') {
            return true;
        }
        return false;
    },

    setHtmlTasksData(data) {

        if (data !== undefined && data !== null && TaskService.isUserLoggedIn()) {
            let totalPages = TaskService.getTotalPages(data) !== undefined ? TaskService.getTotalPages(data) : 1;
            const tpl = document.querySelector('#tpl');
            let out = '';
            out += '<table id="result-table">';
            out += '<tr>';
            out += '<td colspan="7">';
            out += '<div id="paginator-holder">';
            out += '<form id="paginatorForm">';
            out += '<select name="itemsPerPageSelect" id="itemsPerPageSelect">';
            out += '<option value="5"> 5 rows per page </option>';
            out += '<option value="10" class="items-per-pg-opt" > 10 rows per page </option>';
            out += '<option value="15" class="items-per-pg-opt" > 15 rows per page </option>';
            out += '<option value="20" class="items-per-pg-opt" > 20 rows per page </option>';
            out += '<option value="25"> 25 rows per page </option>';
            out += '</select>';
            out += '<span class="text-wrapper"> Page: </span>';
            out += '<input type="number" name="pageNum" min="1" value="1" id="pg-num" />';
            out += `<span class="text-wrapper"> of ${ totalPages }: </span>`;
            out += '<a href="javascript:void(0)" onclick="TaskService.handlePaginator()" class="a-btn"> Go </button>';
            out += '<a href="javascript:void(0)" onclick="TaskService.prev()" class="arrow"> &lt; </a>';
            out += '<a href="javascript:void(0)" onclick="TaskService.next()" class="arrow"> &gt; </a>';
            out += '</form>';
            out += '</div>';
            out += '</td>';
            out += '</tr>';
            out += '<tr>';
            out += '<th> ID </th>';
            out += '<th> Task Name </th>';
            out += '<th> End Date </th>';
            out += '<th> Is Regular </th>';
            out += '<th> Is Closed </th>';
            out += '<th colspan="2"> Actions </th>';
            out += '</tr>';
            for (let i = 0; i < data.length; i++) {
                out += '<tr>';
                out += '<td>';
                out += data[i].taskid;
                out += '</td>';
                out += '<td>';
                out += data[i].taskname;
                out += '</td>';
                out += '<td>';
                out += data[i].enddate;
                out += '</td>';
                out += '<td>';
                out += data[i].isregular;
                out += '</td>';
                out += '<td>';
                out += data[i].isclosed;
                out += '</td>';
                out += '<td>';
                out += '<button';
                out += ' data-taskid="';
                out += data[i].taskid;
                out += '"';
                out += ' data-taskname="';
                out += data[i].taskname;
                out += '"';
                out += ' data-enddate="';
                out += data[i].enddate;
                out += '"';
                out += ' data-isregular="';
                out += data[i].isregular;
                out += '"';
                out += ' data-isclosed="';
                out += data[i].isclosed;
                out += '"';
                out += ' class="form-action-buttons"';
                out += ' onclick="TaskService.handleEditTaskModal(this)"> Edit';
                out += '</button>';
                out += '</td>';
                out += '<td>';
                out += '<button';
                out += ' data-taskid="';
                out += data[i].taskid;
                out += '"';
                out += ' class="form-action-buttons"';
                out += ' onclick="TaskService.handleDeleteTask(this)"> Del';
                out += '</button>';
                out += '</td>';
                out += '</tr>';
            }
            out += '</table>';
            tpl.innerHTML = out;
        }
    },

    getTotalPages(data) {
        if (data !== undefined && data !== null) {
            if (data.length > 0) {
                return data[0].total_pages;
            } else {
                return 1;
            }
        }
        return 1;
    },

    ajaxGetTasks() {
        fetch("/ajax_tasks", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            if (data !== undefined && data !== null) {
                let displTasksBtn = document.querySelector('#displAllTasksBtn');
                if (displTasksBtn !== undefined && displTasksBtn !== null) {
                    displTasksBtn.addEventListener('click', function(event) {
                        event.preventDefault();
                        TaskService.setHtmlTasksData(data);
                    });
                }
            }
        }).catch(function(err) {
            console.log('Error', err);
        });
    },

    ajaxGetTasksData() {
        let fetchPromise = fetch("/ajax_tasks", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(response) {
            return response.json();
        }).catch(function(err) {
            console.log('Error', err);
        });
        return fetchPromise;
    },

    insTaskAjax(input) {

        fetch('/ajax_ins_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(input),
        })
        .then(function(res){
            return res.json();
        }).then(function(data) {
            TaskService.refreshGrid();
            return data;
        }).then(function(data) {
            const modalSelector = document.querySelector("#insTaskAjaxFormModal");
            TaskService.closeModal(modalSelector);
            return data;
        });

    },

    editTask(input) {

        fetch('/ajax_edit_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(input),
        })
        .then(function(res){
            return res.json();
        }).then(function(data) {
            TaskService.refreshGrid();
            return data;
        }).then(function(data) {
            const modalSelector = document.querySelector('#editTaskFormModal');
            TaskService.closeModal(modalSelector);
            return data;
        }).then(function(data) {
            let taskID = parseInt(data.taskID);
            let msg = `A task with ID: ${taskID} has been edited!`;
            window.alert(msg);
        }).catch(function(err) {
            console.log('Error', err);
        });
    },

    deleteTask(taskId) {
        TaskService.ajaxPostDelTask(taskId);
    },

    setDefaultEditFormValues(el) {
        let isValidEl = el !== undefined && el !== null;
        if (isValidEl) {
            const editModForm = document.querySelector('#editTaskForm');
            const taskName = editModForm['taskname'].value = el.dataset.taskname;
            const endDate = editModForm['enddate'].value = el.dataset.enddate;
            const isRegular = editModForm['isregular'].value = el.dataset.isregular;
            const isClosed = editModForm['isclosed'].value = el.dataset.isclosed;
        }
    },

    handleEditTaskModal(el) {

        const editTaskForm = document.querySelector('#editTaskForm');
        const taskId = editTaskForm['taskid'].value = el.dataset.taskid;
        const taskName = editTaskForm['taskname'].value = el.dataset.taskname;
        const endDate = editTaskForm['enddate'].value = el.dataset.enddate;
        const isRegular = editTaskForm['isregular'].value = el.dataset.isregular;
        const isClosed = editTaskForm['isclosed'].value = el.dataset.isclosed;

        const modal = document.getElementById("editTaskFormModal");
        const closeModBtn = document.getElementById("editTaskCloseBtn");
        TaskService.showFormModal(modal, closeModBtn);
    },

    handleDeleteTask(el) {
        let taskId = el.dataset.taskid;
        TaskService.deleteTask(taskId);
    },

    ajaxPostDelTask(taskId) {

        let input = {
            taskid: taskId
        };

        fetch('/ajax_del_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(input),
        })
        .then(function(res){
            return res.json();
        }).then(function(data) {
            let taskID = parseInt(data.taskID);
            let msg = `A task with ID: ${taskID} has been deleted!`;
            window.alert(msg);
        }).then(function(){
            TaskService.refreshGrid();
        }).catch(function(err) {
            console.log('Error', err);
        });
    },

    refreshGrid() {
        TaskService.ajaxGetTasksData().then(function(newData){
            TaskService.setHtmlTasksData(newData);
        });
    },

    showFormModal(modal, closeModBtn) {

        let checkModal = modal !== undefined && modal !== null;
        let checkCloseBtn = closeModBtn !== undefined && closeModBtn !== null;

        if (checkModal) {
            modal.style.display = "block";
        }

        if (checkCloseBtn) {
            closeModBtn.onclick = function() {
              modal.style.display = "none";
            }
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
          if (event.target == modal) {
            if (checkModal) {
              modal.style.display = "none";
            }
          }
        }

    },

    closeModal(modSelector) {
        if (modSelector !== undefined && modSelector !== null) {
            modSelector.style.display = "none";
        }
    },

    liveSearchAjax(input_field) {

        let input_str = input_field.value;

        if (input_str.length > 3) {

            let fetchPromise = fetch("/ajax_tasks_search?search_str=" + input_str, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                if (data !== undefined && data !== null) {
                    TaskService.setHtmlTasksData(data);
                }
            }).catch(function(err) {
                console.log('Error', err);
            });

        }

    },

    paginatedGridAjax(itemsPerPage, pageNum) {

        let isValidInput = itemsPerPage !== undefined && itemsPerPage !== null
            && itemsPerPage !== '' && !isNaN(itemsPerPage)
            && pageNum !== undefined && pageNum !== null && pageNum !== '' && !isNaN(pageNum);

        if (isValidInput) {

            const url = "/ajax_paginated_tasks?items_per_page=" + itemsPerPage + "&page_num=" + pageNum;

            let fetchPromise = fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                if (data !== undefined && data !== null) {
                    TaskService.setHtmlTasksData(data);
                    return data;
                }
            }).then(function(data){
                TaskService.setHtmlTasksData(data);
                return data;
            }).then(function(data) {
                if (data.length > 0) {
                    TaskService.setPaginatorState(data[0].page_num, data[0].total_pages, data[0].items_per_page);
                } else {
                    TaskService.setPaginatorState(pageNum, 1, itemsPerPage);
                }
            }).then(function(){
                TaskService.setPaginatorFormValues();
            }).catch(function(err) {
                console.log('Error', err);
            });

            return fetchPromise;

        }

    },

    setPaginatorFormValues() {

        let pgState = TaskService.getPaginatorState();
        let pageNum = pgState.pageNum;
        let pages = pgState.pages;
        let itemsPerPage = pgState.itemsPerPage;

        const paginatorForm = document.querySelector('#paginatorForm');
        // selectedOpt = paginatorForm['itemsPerPageSelect']; // does not work
        let selectedOpt = document.querySelector('#itemsPerPageSelect');
        selectedOpt.value = itemsPerPage;
        paginatorForm['pageNum'].value = pageNum;
    },

    setPaginatorState(pageNum, totalPages, itemsPerPage) {
        const stateFormSelector = document.querySelector('#stateForm');
        stateFormSelector['pageNum'].value = pageNum;
        stateFormSelector['pages'].value = totalPages;
        stateFormSelector['itemsPerPage'].value = itemsPerPage;
    },

    getPaginatorState() {
        const stateFormSelector = document.querySelector('#stateForm');
        let pageNum = stateFormSelector['pageNum'].value;
        let pages = stateFormSelector['pages'].value;
        let itemsPerPage = stateFormSelector['itemsPerPage'].value;
        pgState = {
            pageNum: parseInt(pageNum),
            pages: parseInt(pages),
            itemsPerPage: parseInt(itemsPerPage)
        };
        return pgState;
    },

    next() {

        let pgState = TaskService.getPaginatorState(); // {pageNum: '1', pages: '3', itemsPerPage: '5'}
        let pageNum = pgState.pageNum;
        let pages = pgState.pages;
        let itemsPerPage = pgState.itemsPerPage;

        let hasErrorMissedClickedGoBtn = isNaN(itemsPerPage) || isNaN(itemsPerPage);

        let newPageNum;

        if ((pageNum + 1) < pages) {
            newPageNum =  pageNum + 1;
            TaskService.paginatedGridAjax(itemsPerPage, newPageNum);
        } else if (hasErrorMissedClickedGoBtn) {
            window.alert("First press 'Go' button to set the paginator");
        } else {
            newPageNum = pages;
            TaskService.paginatedGridAjax(itemsPerPage, newPageNum);
        }

    },

    prev() {

        let pgState = TaskService.getPaginatorState(); // {pageNum: '1', pages: '3', itemsPerPage: '5'}
        let pageNum = pgState.pageNum;
        let pages = pgState.pages;
        let itemsPerPage = pgState.itemsPerPage;
        let newPageNum;
        if ((pageNum - 1) > 0) {
            newPageNum = pageNum - 1;
            TaskService.paginatedGridAjax(itemsPerPage, newPageNum);
        } else {
            newPageNum = 1;
        }

    },

    handleInsTaskTest() {
        const insTaskBtn = document.getElementById("insTaskBtn");
        const insFormModal = document.getElementById("insTaskFormModal");
        const closeInsFormModBtn = document.getElementById("insTaskCloseBtn");

        let isValidInsTaskBtn = insTaskBtn !== undefined && insTaskBtn !== null;
        if (isValidInsTaskBtn) {
            insTaskBtn.addEventListener('click', function(event) {
                event.preventDefault();
                TaskService.showFormModal(insFormModal, closeInsFormModBtn);
            });
        }
    },

    handleInsTaskAjax() {

        const insTaskAjaxBtn = document.querySelector("#insTaskAjaxBtn");
        const insTaskAjaxFormModal = document.querySelector("#insTaskAjaxFormModal");
        const insTaskAjaxCloseBtn = document.querySelector("#insTaskAjaxCloseBtn");

        let isValidInsTaskAjaxBtn = insTaskAjaxBtn !== undefined && insTaskAjaxBtn !== null;
        if (isValidInsTaskAjaxBtn) {
            insTaskAjaxBtn.addEventListener('click', function(event) {
                event.preventDefault();
                TaskService.showFormModal(insTaskAjaxFormModal, insTaskAjaxCloseBtn);
            });
        }

        const sbmInsAjaxTask = document.querySelector('#sbmInsAjaxTask');
        let insValidSbmInsAjaxTask = sbmInsAjaxTask !== undefined && sbmInsAjaxTask !== null;
        if (insValidSbmInsAjaxTask) {
            sbmInsAjaxTask.addEventListener('click', function(event) {
                event.preventDefault();
                const form = document.querySelector('#insTaskAjaxForm');
                const taskName = form['taskname'].value;
                const endDate = form['enddate'].value;
                const isRegular = form['isregular'].value;
                const isClosed = form['isclosed'].value;
                const csrfToken = form['csrfToken'].value;

                const input = {
                    taskname: TaskService.escapeInput(taskName),
                    enddate: TaskService.escapeInput(endDate),
                    isregular: TaskService.escapeInput(isRegular),
                    isclosed: TaskService.escapeInput(isClosed),
                    csrfToken: csrfToken
                };
                TaskService.insTaskAjax(input);
            });
        }
    },

    handleEditTaskAjax() {

        const sbmEditSbmTaskBtn = document.querySelector('#sbmEditTask');
        let isValidEditSbmTaskBtn = sbmEditSbmTaskBtn !== undefined && sbmEditSbmTaskBtn !== null;
        if (isValidEditSbmTaskBtn) {
            sbmEditSbmTaskBtn.addEventListener('click', function(event) {
                event.preventDefault();
                const editTaskForm = document.querySelector('#editTaskForm');
                const taskId = editTaskForm['taskid'].value;
                const taskName = editTaskForm['taskname'].value;
                const endDate = editTaskForm['enddate'].value;
                const isRegular = editTaskForm['isregular'].value;
                const isClosed = editTaskForm['isclosed'].value;
                const csrfToken = editTaskForm['csrfToken'].value;

                const input = {
                    taskid: taskId,
                    taskname: TaskService.escapeInput(taskName),
                    enddate: TaskService.escapeInput(endDate),
                    isregular: TaskService.escapeInput(isRegular),
                    isclosed: TaskService.escapeInput(isClosed),
                    csrfToken: csrfToken
                };
                TaskService.editTask(input);
            });

        }
    },

    handlePaginator() {

        const paginatorForm = document.querySelector('#paginatorForm');
        let opt_value = paginatorForm['itemsPerPageSelect'].value;

        let itemsPerPage = parseInt(opt_value);

        let pgNum = paginatorForm['pageNum'].value;
        let pageNum = parseInt(pgNum);

        let pgState = TaskService.getPaginatorState();
        let pages = pgState.pages;

        if (pageNum === 1) {
            TaskService.paginatedGridAjax(itemsPerPage, pageNum);
        } else if (pageNum > 0) {
            if (pageNum <= pages) {
                TaskService.paginatedGridAjax(itemsPerPage, pageNum);
            } else {
                window.alert(`The page number should be between 1 and ${pages} !`);
            }
        } else {
            window.alert(`The page number should be between 1 and ${pages} !`);
        }

    },

    init() {
        TaskService.ajaxGetTasks();
        TaskService.handleInsTaskTest();
        TaskService.handleInsTaskAjax();
        TaskService.handleEditTaskAjax();
    }

};

// export { TaskService };

TaskService.init();