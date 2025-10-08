import { useEffect, useState } from "react";
import {
    Container,
    Typography,
    Box,
    Paper,
    Divider,
    Stack,
} from "@mui/material";
import TransactionForm from "./components/TransactionForm.jsx";
import TransactionList from "./components/TransactionList.jsx";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import dayjs from "dayjs";
import timezone from "dayjs/plugin/timezone";
import utc from "dayjs/plugin/utc";

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.locale("ja");
dayjs.tz.setDefault("Asia/Tokyo");

const COLORS = ["#1976d2", "#4caf50", "#ffb300", "#e53935"];
const url = "http://localhost:8000/expenses/";

function getCategoryTotal(transactions) {
    return transactions.reduce((acc, tran) => {
        if (!acc[tran.category]) acc[tran.category] = 0;
        acc[tran.category] += tran.amount;
        return acc;
    }, {});
}

export default function App() {
    const [transactions, setTransactions] = useState([]);
    const [totalAmount, setTotalAmount] = useState(0);

    const handleAddTransaction = async ({ amount, type, date, category }) => {
        const adjustedAmount = type === "expense" ? -amount : amount;
        setTotalAmount((prevAmount) => prevAmount + adjustedAmount);
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    amount,
                    category,
                    date: dayjs(date),
                    type,
                }),
            });
            const created = await response.json();
            setTransactions((prev) => [
                ...prev,
                {
                    id: created.expense_id,
                    amount: created.amount,
                    date: created.date,
                    type: created.type,
                    category: created.category,
                },
            ]);
        } catch (e) {
            console.error(e);
        }
    };

    const handleRemoveTransaction = async (id, removeAmount, type) => {
        const adjustedAmount = type === "expense" ? -removeAmount : removeAmount;
        setTransactions(transactions.filter((item) => item.id !== id));
        setTotalAmount((prevAmount) => prevAmount - adjustedAmount);
        try {
            await fetch(`${url}${id}`, { method: "DELETE" });
        } catch (e) {
            console.error(e);
        }
    };

    const categoryData = Object.entries(getCategoryTotal(transactions)).map(
        ([category, amount]) => ({
            name: category,
            value: amount,
        })
    );

    const fetchExpensiveList = async () => {
        const response = await fetch(url);
        const data = await response.json();
        const list = data.map((item) => ({
            id: item.expense_id,
            amount: item.amount,
            date: dayjs(item.date).tz("Asia/Tokyo").format("YYYY-MM-DD"),
            type: item.type,
            category: item.category,
        }));
        const total = data.reduce((sum, item) => sum + item.amount, 0);
        setTotalAmount(total);
        setTransactions(list);
    };

    useEffect(() => {
        fetchExpensiveList();
    }, []);

    return (
        <Box sx={{ backgroundColor: "#f9fafb", minHeight: "100vh", py: 6 }}>
            <Container maxWidth="md">
                {/* タイトル */}
                <Box sx={{ textAlign: "center", mb: 6 }}>
                    <Typography
                        variant="h3"
                        fontWeight={600}
                        gutterBottom
                        sx={{ color: "#1976d2" }}
                    >
                        収支トラッカー
                    </Typography>
                    <Typography variant="h6" color="text.secondary">
                        現在の残高:{" "}
                        <Typography
                            component="span"
                            color="success.main"
                            fontWeight={700}
                            sx={{ fontSize: "1.25rem" }}
                        >
                            ¥{totalAmount.toLocaleString()}
                        </Typography>
                    </Typography>
                </Box>

                {/* フォーム */}
                <Paper elevation={3} sx={{ p: 4, borderRadius: 3, mb: 4 }}>
                    <Typography variant="h6" gutterBottom>
                        新しい取引を追加
                    </Typography>
                    <Divider sx={{ mb: 3 }} />
                    <TransactionForm onAdd={handleAddTransaction} />
                </Paper>

                {/* リスト */}
                <Paper elevation={3} sx={{ p: 4, borderRadius: 3, mb: 4 }}>
                    <Typography variant="h6" gutterBottom>
                        取引リスト
                    </Typography>
                    <Divider sx={{ mb: 3 }} />
                    <TransactionList
                        items={transactions}
                        onRemove={handleRemoveTransaction}
                        setItems={setTransactions}
                    />
                </Paper>

                {/* 円グラフ */}
                <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        カテゴリ別割合
                    </Typography>
                    <Divider sx={{ mb: 3 }} />
                    <Box sx={{ height: 300 }}>
                        <ResponsiveContainer>
                            <PieChart>
                                <Pie
                                    data={categoryData}
                                    dataKey="value"
                                    nameKey="name"
                                    cx="50%"
                                    cy="50%"
                                    outerRadius={100}
                                    label
                                >
                                    {categoryData.map((entry, index) => (
                                        <Cell
                                            key={index}
                                            fill={COLORS[index % COLORS.length]}
                                        />
                                    ))}
                                </Pie>
                            </PieChart>
                        </ResponsiveContainer>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
}
