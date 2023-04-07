/*
Copyright © 2023 Cary Coutant

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.
*/

function init_filters() {
  // Check that all the elements we need are present.
  let filter_div = document.getElementById("issuefilter");
  if (filter_div == null)
    return;
  let select_elem = document.getElementById("by_status");
  if (select_elem == null)
    return;
  let search_box = document.getElementById("search_box");
  let cancel_icon = document.getElementById("search_cancel");
  if (search_box == null || cancel_icon == null)
    return;
  let issue_table = document.getElementById("issueindex");
  if (issue_table == null)
    return;

  // Find the table of issues and make a list for convenient searching.
  let tbody = issue_table.getElementsByTagName("tbody").item(0);
  let trs = tbody.getElementsByTagName("tr");
  let issues = [];
  for (let i = 0; i < trs.length; i++) {
    let tr = trs.item(i);
    let tds = tr.getElementsByTagName("td");
    issues.push({
      "tr":       tr,
      "id":       tr.getAttribute("data-id"),
      "status":   tr.getAttribute("data-status"),
      "title":    tds.item(1).innerHTML.toLowerCase(),
      "author":   tds.item(2).innerHTML.toLowerCase(),
      "champion": tds.item(3).innerHTML.toLowerCase(),
      "type":     tds.item(4).innerHTML.toLowerCase()
    });
  }

  // Stash the list in a global variable.
  window.issues_list = issues;

  // Count the number of open/closed/etc. issues,
  // and show the counts in the filters.
  let open_count = 0,
      accepted_count = 0,
      rejected_count = 0,
      withdrawn_count = 0;
  for (let i = 0; i < issues.length; i++) {
    let status = issues[i].status;
    if (status == "o")
      open_count += 1;
    else if (status == "ca")
      accepted_count += 1;
    else if (status == "cr")
      rejected_count += 1;
    else if (status == "cw")
      withdrawn_count += 1;
  }
  let closed_count = accepted_count + rejected_count + withdrawn_count;
  let total_count = open_count + closed_count;
  let options = select_elem.getElementsByTagName("option");
  for (let i = 0; i < options.length; i++) {
    let o = options.item(i);
    if (o.value == "*")
      o.innerHTML += " (" + total_count + ")";
    else if (o.value == "o")
      o.innerHTML += " (" + open_count + ")";
    else if (o.value == "c")
      o.innerHTML += " (" + closed_count + ")";
    else if (o.value == "ca")
      o.innerHTML += " (" + accepted_count + ")";
    else if (o.value == "cr")
      o.innerHTML += " (" + rejected_count + ")";
    else if (o.value == "cw")
      o.innerHTML += " (" + withdrawn_count + ")";
  }

  // If there are any open issues, default to displaying only those.
  if (open_count > 0)
    select_elem.selectedIndex = 1;

  // Set event handlers.
  select_elem.addEventListener("change", filter_issues);
  search_box.addEventListener("keyup", debounced_filter());
  cancel_icon.addEventListener("click", clear_search_box);

  // Enable the filters.
  filter_div.classList.add("enabled");
  filter_issues();
}

// Match an issue against the current filters.
function check_filter(issue, by_status, search_box) {
  if (by_status != "*" && !issue.status.startsWith(by_status))
    return false;
  search_terms = search_box.toLowerCase().split(/\s+/);
  for (let i = 0; i < search_terms.length; i++) {
    term = search_terms[i];
    if (term.match(/^\d{1,6}(\.\d?)?$/)) {
      if (!issue.id.startsWith(term))
        return false;
    }
    else {
      if (issue.title.indexOf(term) == -1 &&
          issue.author.indexOf(term) == -1 &&
          issue.champion.indexOf(term) == -1 &&
          issue.type.indexOf(term) == -1)
        return false;
    }
  }
  return true;
}

// Filter the table of issues. Hide rows that do not match the
// current filters.
function filter_issues() {
  let by_status = document.getElementById("by_status").value;
  let search_box = document.getElementById("search_box");
  let search_terms = search_box.value;
  let result_div = document.getElementById("resultcount");
  let issue_table = document.getElementById("issueindex");

  let count = 0;
  for (let i = 0; i < window.issues_list.length; i++) {
    let issue = window.issues_list[i];
    if (check_filter(issue, by_status, search_terms)) {
      issue.tr.style.display = "";
      count += 1;
    }
    else
      issue.tr.style.display = "none";
  }
  let total = window.issues_list.length;
  if (count > 0) {
    result_div.innerHTML = "Showing " + count + " of " + total + pluralize(" issue.", " issues.", total);
    issue_table.style.display = "";
  }
  else {
    result_div.innerHTML = "No issues match the filters."
    issue_table.style.display = "none";
  }
  window.setTimeout(function () { search_box.focus(); }, 100);
}

// Debounces calls to filter_issues(), so it doesn't run more often
// than every quarter second.
function debounced_filter() {
  let timer = null;
  return function(e) {
    if (timer)
      window.clearTimeout(timer);
    if (e.code == 'Escape')
      clear_search_box();
    else
      timer = window.setTimeout(function() { filter_issues(); }, 250);
  };
}

// Clear the search box.
function clear_search_box() {
  let search_box = document.getElementById("search_box");
  search_box.value = "";
  filter_issues();
}

function pluralize(singular, plural, count) {
  return (count == 1) ? singular : plural;
}

window.addEventListener("load", function() { init_filters(); });
