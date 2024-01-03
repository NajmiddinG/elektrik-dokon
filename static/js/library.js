var TP = {
    setup: function(tableId, popupId) {
        var table = document.getElementById(tableId);
        var popup = document.getElementById(popupId);

        if (!table || !popup) {
            console.error("Элемент не найден.");
            return;
        }

        var columnNames = Array.from(table.querySelectorAll("thead th"), th => th.textContent);

        table.querySelectorAll("tbody tr").forEach(row => {
            row.addEventListener("click", function() {
                var rowData = Array.from(row.children, cell => cell.textContent.trim());
                var popupContent = "<ul>" + rowData.map((data, index) => `<li><strong>${columnNames[index]}:</strong> ${data}</li>`).join('') + "</ul>";
                popup.innerHTML = popupContent;
                popup.style.display = "block";
            });
        });

        document.addEventListener("click", event => {
            if (!event.target.closest(`#${tableId} tbody, #${popupId}`)) {
                popup.style.display = "none";
            }
        });
    },

    sort: function(tableId, column) {
        var table = document.getElementById(tableId);

        if (!table) {
            console.error("Таблица не найдена.");
            return;
        }

        var rows = table.rows;
        var switching = true;

        while (switching) {
            switching = false;

            for (var i = 1; i < (rows.length - 1); i++) {
                var shouldSwitch = false;
                var x = rows[i].getElementsByTagName("td")[column];
                var y = rows[i + 1].getElementsByTagName("td")[column];

                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }

            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
            }
        }
    }
};

// Пример использования с короткими именами
