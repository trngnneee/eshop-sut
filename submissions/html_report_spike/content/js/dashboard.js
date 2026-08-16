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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 19719, 0, 0.0, 139.95613367817916, 0, 377, 142.0, 228.0, 253.0, 301.0, 133.22748462941695, 54.56209937250862, 35.18088014534491], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["[4] POST /api/cart", 3269, 0, 0.0, 65.39186295503217, 1, 150, 66.0, 102.0, 114.0, 127.0, 22.333811573409854, 6.412246682209469, 8.538693678690988], "isController": false}, {"data": ["[2] GET /api/products?search=", 3321, 0, 0.0, 143.57994579945822, 0, 295, 147.0, 207.0, 225.0, 262.0, 22.52823661092833, 8.545721793067191, 4.08747864235322], "isController": false}, {"data": ["[5] POST /api/apply-coupon", 3260, 0, 0.0, 208.75582822085946, 1, 377, 218.0, 281.0, 306.0, 345.3899999999999, 22.41982848143487, 8.779639864311896, 5.203148533083001], "isController": false}, {"data": ["[6] POST /api/checkout", 3243, 0, 0.0, 148.36540240518042, 5, 310, 155.0, 209.0, 229.0, 267.0, 22.302608504287903, 6.882445593120096, 9.108151672609674], "isController": false}, {"data": ["[1] POST /api/login", 3343, 0, 0.0, 142.57403529763738, 2, 313, 146.0, 208.0, 228.0, 269.55999999999995, 22.665943453793474, 14.209259155281714, 5.090983392941894], "isController": false}, {"data": ["[3] GET /api/products/4", 328, 0, 0.0, 131.2621951219512, 1, 258, 133.0, 194.0, 213.65000000000003, 248.83999999999992, 2.352063792559447, 1.1002329654648195, 0.3744007794796776], "isController": false}, {"data": ["[3] GET /api/products/5", 329, 0, 0.0, 132.30091185410325, 1, 263, 134.0, 197.0, 221.5, 255.5999999999999, 2.375125434055978, 1.1272567978039114, 0.3780717243663324], "isController": false}, {"data": ["[3] GET /api/products/6", 329, 0, 0.0, 131.29179331306995, 1, 300, 135.0, 193.0, 213.0, 256.9999999999999, 2.3617751360353765, 1.0932435688288755, 0.37594662809938123], "isController": false}, {"data": ["[3] GET /api/products/7", 328, 0, 0.0, 131.31707317073187, 1, 310, 133.0, 193.20000000000005, 216.0, 271.61999999999955, 2.351136502111005, 1.0791349179611058, 0.3742531736758729], "isController": false}, {"data": ["[3] GET /api/products/8", 328, 0, 0.0, 132.98780487804882, 1, 295, 135.0, 194.20000000000005, 219.75000000000006, 263.71, 2.350883731597884, 1.0606526210920142, 0.3742129377445851], "isController": false}, {"data": ["[3] GET /api/products/9", 328, 0, 0.0, 130.90243902439022, 1, 300, 133.0, 195.0, 217.10000000000002, 244.41999999999996, 2.3522999469298185, 1.0888575926218105, 0.3744383704585551], "isController": false}, {"data": ["[3] GET /api/products/10", 328, 0, 0.0, 131.62500000000009, 1, 300, 134.0, 198.20000000000005, 220.0, 252.22999999999973, 2.3678891134854174, 1.061387795986139, 0.3792322408316488], "isController": false}, {"data": ["[3] GET /api/products/1", 329, 0, 0.0, 131.3525835866261, 1, 267, 135.0, 196.0, 217.5, 244.49999999999994, 2.3614530472793045, 1.0631150925739838, 0.37589535811184244], "isController": false}, {"data": ["[3] GET /api/products/2", 328, 0, 0.0, 129.6158536585366, 1, 266, 133.5, 193.0, 215.55, 240.25999999999988, 2.3510016844066945, 1.0492263376697848, 0.37423171343583134], "isController": false}, {"data": ["[3] GET /api/products/3", 328, 0, 0.0, 129.80487804878047, 1, 258, 134.0, 192.10000000000002, 210.10000000000002, 242.9399999999997, 2.3505467887804388, 1.0788642487566467, 0.37415930329219876], "isController": false}]}, function(index, item){
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
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 19719, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
