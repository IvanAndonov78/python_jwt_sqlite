def render():
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
            </nav>
            <div id="context-nav"></div>
        </div>

        <div class="second-column">
            <div id="tpl"> </div>
        </div> 
    </div>
    """
    return html

