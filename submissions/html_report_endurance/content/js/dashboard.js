/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 100.0, "KoPercent": 0.0};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [1.0, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "[4] POST /api/cart"], "isController": false}, {"data": [1.0, 500, 1500, "[2] GET /api/products?search="], "isController": false}, {"data": [1.0, 500, 1500, "[5] POST /api/apply-coupon"], "isController": false}, {"data": [1.0, 500, 1500, "[6] POST /api/checkout"], "isController": false}, {"data": [1.0, 500, 1500, "[1] POST /api/login"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/4"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/5"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/6"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/7"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/8"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/9"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/10"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/1"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/2"], "isController": false}, {"data": [1.0, 500, 1500, "[3] GET /api/products/3"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 25624, 0, 0.0, 8.751131751482975, 0, 125, 3.0, 32.0, 44.0, 51.0, 28.529342669426374, 11.655504589645755, 7.550169850155261], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["[4] POST /api/cart", 4269, 0, 0.0, 2.138908409463573, 1, 17, 2.0, 3.0, 4.0, 5.0, 4.7618410221059175, 1.3671691997061914, 1.8205568002079193], "isController": false}, {"data": ["[2] GET /api/products?search=", 4276, 0, 0.0, 2.095182413470534, 0, 51, 1.0, 3.0, 4.0, 15.0, 4.767160551634949, 1.8089667070108253, 0.8649813312457496], "isController": false}, {"data": ["[5] POST /api/apply-coupon", 4267, 0, 0.0, 7.899460979610954, 1, 118, 3.0, 31.0, 35.0, 43.0, 4.764627193325279, 1.8658354536361688, 1.1057700897094325], "isController": false}, {"data": ["[6] POST /api/checkout", 4267, 0, 0.0, 31.038668853995585, 5, 125, 42.0, 48.0, 50.0, 63.0, 4.764611232512358, 1.46567630687636, 1.9458451706528086], "isController": false}, {"data": ["[1] POST /api/login", 4276, 0, 0.0, 5.905519176800747, 2, 100, 4.0, 8.0, 16.0, 33.0, 4.766809804734704, 2.9883289766241266, 1.070670170985334], "isController": false}, {"data": ["[3] GET /api/products/4", 427, 0, 0.0, 2.964871194379392, 1, 32, 2.0, 3.0, 10.0, 28.039999999999793, 0.47994029407863825, 0.22450332115592553, 0.07639674603009575], "isController": false}, {"data": ["[3] GET /api/products/5", 427, 0, 0.0, 2.925058548009368, 1, 35, 2.0, 4.0, 6.0, 27.919999999999675, 0.4805181944219377, 0.22805843993072436, 0.0764887360261483], "isController": false}, {"data": ["[3] GET /api/products/6", 427, 0, 0.0, 3.3512880562060863, 1, 39, 2.0, 4.0, 15.0, 31.0, 0.4811820626145202, 0.2227346657024244, 0.07659441035758476], "isController": false}, {"data": ["[3] GET /api/products/7", 427, 0, 0.0, 2.941451990632319, 1, 64, 2.0, 3.0, 4.0, 29.039999999999793, 0.4815217440334156, 0.22101095673408722, 0.07664848073969407], "isController": false}, {"data": ["[3] GET /api/products/8", 427, 0, 0.0, 4.725995316159252, 1, 64, 2.0, 10.0, 23.0, 37.0, 0.4818700621014274, 0.21740621942466748, 0.07670392590091081], "isController": false}, {"data": ["[3] GET /api/products/9", 427, 0, 0.0, 4.484777517564396, 1, 82, 2.0, 7.0, 19.599999999999966, 35.0, 0.48219764683031274, 0.22320477011481274, 0.07675607073568455], "isController": false}, {"data": ["[3] GET /api/products/10", 426, 0, 0.0, 3.866197183098592, 1, 48, 2.0, 4.0, 17.0, 35.0, 0.4827102480745413, 0.21637109752560005, 0.07730906316818825], "isController": false}, {"data": ["[3] GET /api/products/1", 427, 0, 0.0, 3.629976580796255, 1, 39, 2.0, 5.0, 12.199999999999932, 32.71999999999997, 0.4774668093476149, 0.21495331944262738, 0.07600301750357541], "isController": false}, {"data": ["[3] GET /api/products/2", 427, 0, 0.0, 3.224824355971894, 0, 38, 2.0, 4.0, 6.599999999999966, 28.319999999999823, 0.47861584745268765, 0.21360101785730298, 0.0761859210300665], "isController": false}, {"data": ["[3] GET /api/products/3", 427, 0, 0.0, 2.4332552693208442, 1, 16, 2.0, 3.0, 4.0, 6.0, 0.47930136494252873, 0.21999183742479347, 0.07629504148987518], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": []}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 25624, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
