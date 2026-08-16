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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 155778, 0, 0.0, 5.513743917626259, 0, 140, 4.0, 13.0, 18.0, 28.0, 273.77648739800037, 111.95361915352805, 72.39689697397351], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["[4] POST /api/cart", 25962, 0, 0.0, 2.248979277405448, 0, 88, 2.0, 4.0, 6.0, 10.0, 45.71482905802307, 13.125155999080842, 17.477867389666002], "isController": false}, {"data": ["[2] GET /api/products?search=", 26124, 0, 0.0, 4.139144082070117, 0, 114, 3.0, 11.0, 15.950000000000728, 25.0, 45.91785618240589, 17.42568327946018, 8.331589720004606], "isController": false}, {"data": ["[5] POST /api/apply-coupon", 25801, 0, 0.0, 5.973140575946661, 0, 140, 5.0, 14.0, 19.0, 34.0, 45.50898414831826, 17.821389300269164, 10.56172747690244], "isController": false}, {"data": ["[6] POST /api/checkout", 25797, 0, 0.0, 10.677830755514213, 3, 125, 10.0, 21.0, 25.0, 34.0, 45.50249058094741, 14.026860229814298, 18.583091968273315], "isController": false}, {"data": ["[1] POST /api/login", 26127, 0, 0.0, 6.377540475370324, 1, 128, 6.0, 13.0, 17.0, 29.0, 45.91764104204415, 28.78594304429549, 10.313532655927888], "isController": false}, {"data": ["[3] GET /api/products/4", 2597, 0, 0.0, 3.679630342703122, 0, 52, 2.0, 7.0, 12.0, 23.0, 4.586329664740538, 2.1453631927839036, 0.7300505228053785], "isController": false}, {"data": ["[3] GET /api/products/5", 2598, 0, 0.0, 3.7956120092378747, 0, 128, 2.0, 8.0, 12.0, 24.0, 4.593019247190356, 2.1798899942719854, 0.7311153684492461], "isController": false}, {"data": ["[3] GET /api/products/6", 2597, 0, 0.0, 3.708894878706199, 0, 121, 2.0, 8.0, 12.0, 22.0, 4.596801886157909, 2.1278164980848135, 0.7317174877380266], "isController": false}, {"data": ["[3] GET /api/products/7", 2597, 0, 0.0, 3.6707739699653406, 0, 122, 2.0, 7.0, 11.0, 23.0, 4.597428484937535, 2.1101478397662516, 0.7318172295359554], "isController": false}, {"data": ["[3] GET /api/products/8", 2597, 0, 0.0, 3.6592221794378084, 0, 88, 2.0, 7.0, 11.0, 23.0, 4.600996026170933, 2.075840003995089, 0.732385109634631], "isController": false}, {"data": ["[3] GET /api/products/9", 2596, 0, 0.0, 3.658320493066253, 0, 87, 2.0, 7.0, 12.0, 23.0, 4.600153456582951, 2.1293679086135926, 0.732250989670919], "isController": false}, {"data": ["[3] GET /api/products/10", 2595, 0, 0.0, 3.718304431599228, 0, 89, 2.0, 7.0, 12.0, 25.0, 4.602900093122257, 2.0632140065850737, 0.7371832180391114], "isController": false}, {"data": ["[3] GET /api/products/1", 2597, 0, 0.0, 3.6915671929149028, 0, 93, 2.0, 8.0, 12.0, 22.0, 4.572794951437164, 2.0586508521606763, 0.7278960713713455], "isController": false}, {"data": ["[3] GET /api/products/2", 2596, 0, 0.0, 3.6825885978428428, 0, 87, 2.0, 7.0, 12.0, 22.0, 4.575328124697078, 2.0419188994009425, 0.728299301099242], "isController": false}, {"data": ["[3] GET /api/products/3", 2597, 0, 0.0, 3.784366576819405, 0, 57, 2.0, 8.0, 13.0, 23.019999999999982, 4.581200320348856, 2.1026993657851194, 0.7292340353680308], "isController": false}]}, function(index, item){
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
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 155778, 0, "", "", "", "", "", "", "", "", "", ""], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
