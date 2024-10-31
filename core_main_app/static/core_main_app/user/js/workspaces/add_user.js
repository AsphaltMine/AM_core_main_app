
var addUserSelected = [];
var addUserSearchTimer = null;

load_form_add_user = function() {
    $("#banner_rights_errors").hide();
    $("#user-rights").show()
    $('#add-user-yes').show();
    addUserSelected = [];
    $("#add-user-chips").empty();
    $("#add-user-search").val("");
    $("#add-user-options").hide().empty();
    $("#write").prop("checked", false);
    $("#add-user-modal").modal("show");
};

renderAddUserChips = function() {
    var chips = $("#add-user-chips");
    chips.empty();
    addUserSelected.forEach(function(user) {
        var chip = $('<span class="am-user-tag-chip"></span>').attr("data-user-id", user.id);
        chip.append($('<span class="am-user-tag-chip-text"></span>').text(user.username));
        var removeBtn = $('<button type="button" aria-label="Remove"></button>').html("&times;");
        removeBtn.on("click", function() { removeAddUserChip(user.id); });
        chip.append(removeBtn);
        chips.append(chip);
    });
};

removeAddUserChip = function(userId) {
    addUserSelected = addUserSelected.filter(function(u) { return u.id !== userId; });
    renderAddUserChips();
};

searchAddUserOptions = function(query) {
    $.ajax({
        url: searchUsersForWorkspaceUrl,
        type: "POST",
        dataType: "json",
        data: { workspace_id: workspace_id, query: query },
        success: function(data) {
            var options = $("#add-user-options");
            options.empty();
            var selectedIds = addUserSelected.map(function(u) { return u.id; });
            var matches = (data.users || []).filter(function(u) { return selectedIds.indexOf(u.id) === -1; });
            if (!matches.length) {
                options.append($('<div class="am-user-tag-empty"></div>').text("No users found"));
            } else {
                matches.forEach(function(user) {
                    var opt = $('<div class="am-user-tag-option"></div>').text(user.username);
                    opt.on("click", function() {
                        addUserSelected.push(user);
                        $("#add-user-search").val("");
                        options.hide().empty();
                        renderAddUserChips();
                        $("#add-user-search").focus();
                    });
                    options.append(opt);
                });
            }
            options.show();
        }
    });
};

add_user_from_form = function() {
    var write = document.getElementById("write").checked;
    call_ajax_add_user(addUserSelected.map(function(u) { return u.id; }), write)
};

call_ajax_add_user = function(selected, write) {
    event.preventDefault()
    $("#banner_rights_errors").hide();
    $("#form_edit_rights_errors").html("");
    $.ajax({
        url : addUserToWorkspaceUrl,
        type : "POST",
        dataType: "json",
        data : {
            workspace_id: workspace_id,
            users_id: selected,
            write: write
        },
        success: function(data){
           location.reload();
        },
        error:function(data){
            $("#form_edit_rights_errors").html(data.responseText);
            $("#banner_rights_errors").show(500);
        }
    });
};

$('.add-user-btn').on('click', load_form_add_user);
$('#add-user-yes').on('click', add_user_from_form);

$(document).on("input", "#add-user-search", function() {
    var query = $(this).val();
    clearTimeout(addUserSearchTimer);
    addUserSearchTimer = setTimeout(function() { searchAddUserOptions(query); }, 200);
});
$(document).on("focus click", "#add-user-search", function() {
    searchAddUserOptions($(this).val());
});
$(document).on("keydown", "#add-user-search", function(e) {
    if (e.key === "Escape") {
        $("#add-user-options").hide().empty();
        $(this).blur();
    } else if (e.key === "Backspace" && !$(this).val() && addUserSelected.length) {
        removeAddUserChip(addUserSelected[addUserSelected.length - 1].id);
    }
});
$(document).on("click", function(e) {
    if (!$(e.target).closest("#add-user-tags").length) {
        $("#add-user-options").hide().empty();
    }
});
