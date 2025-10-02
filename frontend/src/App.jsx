import { useState } from "react";
import { Container, Typography, Box, Stack } from "@mui/material";
import TransactionForm from './components/TransactionForm.jsx'
import TransactionList from "./components/TransactionList.jsx";
import { PieChart, Pie, Sector, Cell, ResponsiveContainer } from "recharts";
import dayjs from "dayjs";
import timezone from 'dayjs/plugin/timezone';
import utc from 'dayjs/plugin/utc';

// rechartsの処理
const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];
const RADIAN = Math.PI / 180;
const customizedLabel = ({
  cx,
  cy,
  midAngle,
  innerRadius,
  outerRadius,
  percent,
}) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
  const x = cx + radius * Math.cos(-midAngle * RADIAN);
  const y = cy + radius * Math.sin(-midAngle * RADIAN);

  return (
    <text
      x = {x}
      y = {y}
      fill="white"
      textAnchor={x > cx ? "start" : "middle"}
      dominantBaseline="central"
      fontSize={16}
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

// dayjsの処理
// UTCプラグインを読み込み
dayjs.extend(utc);
// timezoneプラグインを読み込み
dayjs.extend(timezone);
// 日本語化
dayjs.locale('ja');
// タイムゾーンのデフォルトをJST化
dayjs.tz.setDefault('Asia/Tokyo');

// 月ごとの集計
function getMonthlyTotal(transactions, year, month) {
  return transactions
    .filter(tran => {
      const date = new Date(tran.date);
      return date.getFullYear() === year && date.getMonth() + 1 === month;
    })
    .reduce((sum, tran) => sum + tran.amount, 0); //  1行アロー関数なのでreturn省略
}

//  カテゴリ集計
function getCategoryTotal(transactions) {
  return transactions.reduce((acc, tran) => {
    if (!acc[tran.category]) acc[tran.category] = 0;  //  accオブジェクトにはtran.categoryがないので作成して値を0入れておく例{交通費:0}
    acc[tran.category] += tran.amount;
    return acc;
  }, {});
}

function App() {
  const [transactions, setTransactions] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);

  const handleAddTransaction = ({amount, type, date, category}) => {
    const adjustedAmount = type === "expense" ? -amount : amount
    //  登録処理
    setTransactions([
      ...transactions,
      {id: `${date}-${Date.now()}`, amount: adjustedAmount, date: dayjs(date).tz("Asia/Tokyo").format("YYYY-MM-DD"), type, category}
    ]);
      setTotalAmount(prevAmount => prevAmount + adjustedAmount)
  }

  //  削除処理
  const handleRemoveTransaction = (id, removeAmount) => {
    setTransactions(transactions.filter((item) => item.id !== id));
    setTotalAmount(prevAmount => prevAmount - removeAmount)
  }

  //  グラフ用にオブジェクトを配列に変換
  const categoryData = Object.entries(getCategoryTotal(transactions)).map(
    ([category, amount]) => ({
      name: category,
      value: amount
    })
  );

  return (
    <>
    <Container maxWidth="sm">
      <Typography variant="h4" component="h4" gutterBottom>
        収支トラッカー
      </Typography>
      <Stack spacing={2}>
      <Box><Typography variant="h5">残高: ¥{totalAmount}</Typography></Box>
      <TransactionForm onAdd={handleAddTransaction} />
      <TransactionList items={transactions} onRemove={handleRemoveTransaction} setItems={setTransactions} />
      </Stack>
    </Container>

     <ResponsiveContainer width="100%" height={500}>
        <PieChart width={500} height={500}>
          <Pie
            data={categoryData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            fill="#8884d8"
            label={customizedLabel}
            labelLine={false}
            isAnimationActive={false}
          >
            {categoryData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
      </>
  );
}

export default App;