<template>
  <div>
    <el-table :data="tableData" :span-method="arraySpanMethod" border style="width: 100%">
      <el-table-column prop="id" label="ID" width="180"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="amount1" label="数值 1（元）"></el-table-column>
      <el-table-column prop="amount2" label="数值 2（元）"></el-table-column>
      <el-table-column prop="amount3" sortable label="数值 3"></el-table-column>
    </el-table>

    <!--    <el-table :data="tableData" border :show-header=true style="width: 100%; margin-top: 20px">-->
    <!--      <el-table-column prop="id" label="ID" width="180"></el-table-column>-->
    <!--      <el-table-column prop="name" label="姓名"></el-table-column>-->
    <!--      <el-table-column prop="amount1" label="数值 1（元）"></el-table-column>-->
    <!--      <el-table-column prop="amount2" label="数值 2（元）"></el-table-column>-->
    <!--      <el-table-column prop="amount3" :label=columnName></el-table-column>-->
    <!--    </el-table>-->

    <el-table :data="dataList" :span-method="excelSpanMethod" border style="width: 100%">
      <!-- 动态生成列 -->
      <el-table-column v-for="(item,index) in headerList" :prop="item" :label="item">
        <template slot-scope="scope">
          <div>{{ scope.row[item][0] }}</div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
  import qs from 'qs'

  export default {
    name: "Excel",
    data() {
      return {
        headerList: [],
        dataList: [],

        tableData: [{
          id: '12987122',
          name: '王小虎',
          amount1: '234',
          amount2: '3.2',
          amount3: 10
        }, {
          id: '12987123',
          name: '王小虎',
          amount1: '165',
          amount2: '4.43',
          amount3: 12
        }, {
          id: '12987124',
          name: '王小虎',
          amount1: '324',
          amount2: '1.9',
          amount3: 9
        }, {
          id: '12987125',
          name: '王小虎',
          amount1: '621',
          amount2: '2.2',
          amount3: 17
        }, {
          id: '12987126',
          name: '王小虎',
          amount1: '539',
          amount2: '4.1',
          amount3: 15
        }],
        columnName: '自定义列名'
      }
    },
    methods: {
      excelSpanMethod({row, column, rowIndex, columnIndex}) {
        if (rowIndex >= this.dataList.length || columnIndex >= this.dataList[rowIndex].length) {
          return [1, 1]
        }

        let data = this.dataList[rowIndex][this.headerList[columnIndex]]
        if (data[1] === 1) {
          return [data[2], data[3]]
        } else if (data[1] === -1) {
          return [0, 0]
        }

        return [1, 1]
      },

      arraySpanMethod({row, column, rowIndex, columnIndex}) {
        if (rowIndex === 0 && columnIndex === 0) {
          return [2, 2]
        } else if (rowIndex === 0 && columnIndex === 1) {
          return [1, 0]
        } else if (rowIndex === 1 && columnIndex === 0) {
          return [0, 0]
        } else if (rowIndex === 1 && columnIndex === 1) {
          return [0, 0]
        }
        return [1, 1]
      },

      listSheetNames(path) {
        this.axios.post("/api/hello/sheet/names", {
          "path": path
        }).then(res => {
          res = res['data']
          if (res['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          }

          console.info('sheets ' + res['data'])
          this.listSheetData(path, res['data'][0])
        }).catch(res => {
          this.$message.error(res['data']['msg'])
        })
      },

      listSheetData(path, sheet) {
        this.axios.post("/api/hello/sheet/data", {
          "path": path, "sheet": sheet
        }).then(res => {
          res = res['data']
          if (res['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          }

          // 提取表头列表&数据
          let headerList = [], dataList = []
          for (const v of res['data'][0]) {
            headerList.push(v[0])
          }
          for (let i = 1; i < res['data'].length; i++) {
            let data = {}
            for (let j = 0; j < res['data'][i].length; j++) {
              data[headerList[j]] = res['data'][i][j]
            }
            dataList.push(data)
          }

          console.info(headerList)
          console.info(dataList)

          this.dataList = dataList;
          this.headerList = headerList;
        }).catch(res => {
          this.$message.error(res)
        })
      }
    }
  }
</script>

<style scoped>

</style>
