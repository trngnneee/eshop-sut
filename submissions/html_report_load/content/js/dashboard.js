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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 8040, 0, 0.0, 2.744776119402989, 0, 37, 2.0, 6.0, 7.0, 10.0, 26.97144850768049, 11.019002458964149, 7.135029483248516], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["[4] POST /api/cart", 1340, 0, 0.0, 1.4798507462686559, 0, 5, 1.0, 2.0, 2.0, 3.0, 4.5190118876991825, 1.2974506786948825, 1.7277276894865528], "isController": false}, {"data": ["[2] GET /api/products?search=", 1345, 0, 0.0, 0.9903345724907078, 0, 9, 1.0, 1.0, 2.0, 3.0, 4.5196259295476, 1.7151594491264857, 0.8200879100846463], "isController": false}, {"data": ["[5] POST /api/apply-coupon", 1335, 0, 0.0, 2.3056179775280916, 1, 19, 2.0, 3.0, 4.0, 5.0, 4.5174607471575525, 1.7690446871193153, 1.0484068601532892], "isController": false}, {"data": ["[6] POST /api/checkout", 1335, 0, 0.0, 6.8711610486891415, 4, 27, 6.0, 10.0, 11.0, 14.0, 4.517659480147679, 1.3860513985286305, 1.844899322393378], "isController": false}, {"data": ["[1] POST /api/login", 1345, 0, 0.0, 3.19628252788104, 2, 37, 3.0, 4.0, 4.0, 5.0, 4.519003332974949, 2.8329506162391813, 1.0150105142424202], "isController": false}, {"data": ["[3] GET /api/products/4", 134, 0, 0.0, 1.5149253731343273, 1, 4, 1.0, 2.0, 2.0, 3.6500000000000057, 0.4627407374153512, 0.2164578254120637, 0.07365892597529516], "isController": false}, {"data": ["[3] GET /api/products/5", 134, 0, 0.0, 1.611940298507463, 1, 5, 2.0, 2.0, 2.0, 4.650000000000006, 0.46425737874740586, 0.2203409043664446, 0.07390034446858121], "isController": false}, {"data": ["[3] GET /api/products/6", 134, 0, 0.0, 1.649253731343284, 1, 4, 2.0, 2.0, 3.0, 3.6500000000000057, 0.46510982145336405, 0.2152949759461861, 0.07403603603212729], "isController": false}, {"data": ["[3] GET /api/products/7", 134, 0, 0.0, 1.6641791044776117, 1, 3, 2.0, 2.0, 2.0, 3.0, 0.4663075402625242, 0.21402787492518202, 0.07422668853788228], "isController": false}, {"data": ["[3] GET /api/products/8", 134, 0, 0.0, 1.6417910447761188, 1, 7, 2.0, 2.0, 2.0, 5.600000000000023, 0.46768766840246273, 0.21100752226751734, 0.07444637690390762], "isController": false}, {"data": ["[3] GET /api/products/9", 134, 0, 0.0, 1.6044776119402988, 1, 4, 2.0, 2.0, 3.0, 3.6500000000000057, 0.4693388626588397, 0.21725255947293948, 0.07470921348963952], "isController": false}, {"data": ["[3] GET /api/products/10", 134, 0, 0.0, 1.6044776119402986, 1, 3, 2.0, 2.0, 2.0, 3.0, 0.4707221369379876, 0.21099752036575814, 0.07538909224397458], "isController": false}, {"data": ["[3] GET /api/products/1", 134, 0, 0.0, 1.6791044776119395, 1, 4, 2.0, 2.0, 3.0, 3.6500000000000057, 0.45389571237915877, 0.2043417220769455, 0.07225097765410438], "isController": false}, {"data": ["[3] GET /api/products/2", 134, 0, 0.0, 1.7761194029850749, 1, 3, 2.0, 3.0, 3.0, 3.0, 0.45827319922572346, 0.20452231645132388, 0.0729477846423759], "isController": false}, {"data": ["[3] GET /api/products/3", 134, 0, 0.0, 1.6940298507462688, 1, 3, 2.0, 2.0, 3.0, 3.0, 0.46003529225973455, 0.2111490110957766, 0.07322827406087572], "isController": false}]}, function(index, item){
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
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 8040, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
