def render(csrf_token):
    html = ''
    html += f"""
    <div class="row">
        <div class="first-column">
            <p> Search by Task Name or Date:</p>
            <input
                type="text"
                id="search-input"
                onkeyup="TaskService.liveSearchAjax(this)"
                placeholder="Search item "
                />
            <div class="sep20"></div>
            <nav class="tpl-nav">
                <a href="javascript:void(0)" id="displAllTasksBtn"> Display All Tasks </a>
                <a href="javascript:void(0)" id="insTaskAjaxBtn"> Insert Task </a>
                <a href="javascript:void(0)" id="insTaskBtn"> Insert Task (Test) </a>
            </nav>
            <div id="context-nav"></div>
        </div>

        <div class="second-column">

            <div id="insTaskFormModal" class="modal">
              <div id="ins-task-form-modal" class="modal-content">
                <p><span id="insTaskCloseBtn" class="close"> &times; </span></p>
                <div style="width:100%;">
                  <form id="insTaskForm" method="POST" action="/ins_task" class="common-form">
                    <h3> Insert New Task: </h3>
                    <label> Task Name: </label>
                    <input type="text" name="taskname" />
                    <label> End Date: </label>
                    <input type="date" name="enddate" />
                    <!--<input type="text" name="enddate" />-->
                    <label> Is Regular: </label>
                    <input type="number" min="0" max="1" name="isregular" />
                    <label> Is Closed:</label>
                    <input type="number" min="0" max="1" name="isclosed" />
                    <input type="hidden" name="csrfToken" value="{csrf_token}" />
                    <input type="submit" name="sbmInsTask" value="Save" />
                    <input type="reset" name="rstInsTask" value="Clear" />
                  </form>
                </div>
              </div>
            </div>

            <div id="insTaskAjaxFormModal" class="modal">
              <div id="ins-task-ajax-form-modal" class="modal-content">
                <p><span id="insTaskAjaxCloseBtn" class="close"> &times; </span></p>
                <div style="width:100%;">
                  <form id="insTaskAjaxForm" class="common-form">
                    <h3> Insert New Task: </h3>
                    <label> Task Name: </label>
                    <input type="text" name="taskname" />
                    <label> End Date: </label>
                    <input type="date" name="enddate" />
                    <!-- <input type="text" name="enddate" />-->
                    <label> Is Regular: </label>
                    <input type="number" min="0" max="1" name="isregular" />
                    <label> Is Closed: </label>
                    <input type="number" min="0" max="1" name="isclosed" />
                    <input type="hidden" name="csrfToken" value="{csrf_token}" />
                    <button id="sbmInsAjaxTask" class="ajax-form-sbm-rst"> Save </button>
                    <button id="rstInsAjaxTask" class="ajax-form-sbm-rst"> Clear </button>
                  </form>
                </div>
              </div>
            </div>

            <div id="editTaskFormModal" class="modal">
              <div id="edit-task-form-modal" class="modal-content">
                <p><span id="editTaskCloseBtn" class="close"> &times; </span></p>
                <div style="width:100%;">
                <form id="editTaskForm" class="common-form">
                  <h3> Edit Task: </h3>
                  <label> Task ID (read only): </label>
                  <input type="number" name="taskid" readonly style="background:silver;" />
                  <label> Task Name: </label>
                  <input type="text" name="taskname" />
                  <label> End Date: </label>
                  <input type="date" name="enddate" />
                  <!-- <input type="text" name="enddate" /> -->
                  <label> Is Regular: </label>
                  <input type="number" min="0" max="1" name="isregular" />
                  <label> Is Closed:</label>
                  <input type="number" min="0" max="1" name="isclosed" />
                  <input type="hidden" name="csrfToken" value="{csrf_token}" />
                  <button id="sbmEditTask" class="ajax-form-sbm-rst"> Edit </button>
                  <button id="rstEditTask" class="ajax-form-sbm-rst"> Clear </button>
                </form>
              </div>
            </div>

            </div>
            <!-- ----------------------------------- -->
            <div id="tpl"> </div>
        </div> <!-- end of div class="second-column" -->
    </div>
    """
    return html

