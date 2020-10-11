<template>
  <div>

    <!--https://element.eleme.cn/#/zh-CN/component/table-->
    <el-table v-if="dataList.length!==0" :data="dataList" :span-method="excelSpanMethod" border style="width: 100%">
      <!-- 动态生成列 -->
      <el-table-column v-for="(item, index) in headerList" :prop="item" :label="item">
        <template slot-scope="scope">
          <div>{{ scope.row[item][0] }}</div>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
  export default {
    name: "Excel",
    data() {
      return {
        headerList: [],
        dataList: [],
        tableData: []
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

      // 获取excel文件sheet名称列表
      listSheetNames(path) {
        this.axios.post("/api/hello/sheet/names", {
          "path": path
        }).then(res => {
          res = res['data']
          if (res['code'] !== 0) {
            this.$message.error(res['msg'])
            return
          }

          // 默认展示第一个sheet内容
          this.listSheetData(path, res['data'][0])
        }).catch(res => {
          this.$message.error(res['data']['msg'])
        })
      },

      // 获取excel某个sheet内容
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
