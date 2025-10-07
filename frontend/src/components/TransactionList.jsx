import { IconButton, Typography,  Card, CardContent, List, ListItem, ListItemText, Button } from "@mui/material";
import DeleteIcon from '@mui/icons-material/Delete';
import { useState } from "react";
import dayjs from "dayjs";

export default function TransactionList({ items, onRemove, setItems }) {
    //  次のソート方向（降順であればtrue）
    const [desc, setDesc] = useState(true);

    //  ソートの処理
    const handleSort = e => {
        //  既存のTodoリストを複製の上でソート
        const sorted = [...items];       //  あらかじめ複製しないと動かないため
        sorted.sort((a,b) => {
            //  desc値に応じて昇順/降順を決定
            const dateA = dayjs(a.date);
            const dateB = dayjs(b.date);
            return desc ? dateB.diff(dateA) : dateA.diff(dateB);
        });
        //  desc値を反転
        setDesc(d => !d);
        //  ソート済みのリストを再セット
        setItems(sorted);
    };

    return (
        <>
            {items.length === 0 ? (
            <Typography color="text.secondary">まだ記録がありません</Typography>
        ) : (
            <>
                <Button variant="contained" color="primary" onClick={handleSort}>
                    {desc ? "日付昇順" : "日付降順"}
                </Button>
                <Card sx={{ mt: 3, mb: 3}}>
                    <CardContent>
                        <Typography variant="h6">取引リスト</Typography>
                        <List>
                            {items.map(item => (
                                <ListItem key={item.id}>
                                    <ListItemText primary={`金額:${item.amount} (${item.type === "income" ? "収入" : "支出"}:${item.category}) 日付:(${item.date})`} />
                                    <IconButton onClick={() => onRemove(item.id, item.amount, item.type)} aria-label="削除"><DeleteIcon /></IconButton>
                                </ListItem>
                            ))}
                        </List>
                    </CardContent>
                </Card>
            </>
            )}
        </>
    );
}