import { useState } from "react";
import { Button, TextField, Typography, Stack, Alert, Select, InputLabel, FormControl, MenuItem } from "@mui/material";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

export default function TransactionForm({onAdd}) {  //  親から子に渡されたpropsはオブジェクトなので分割代入でかくとそのまま使えるprops.onAddと書かなくていい
    const [amount, setAmount] = useState('');
    const [type, setType] = useState('income'); //  収支管理
    const [errorMessage, setErrorMessage] = useState(''); // エラーメッセージ用のstate
    const [date, setDate] = useState(null)
    const [category, setCategory] = useState('');

    //  登録処理
    const handleRegister = () => {
        const parsedAmount = parseFloat(amount);
        if (amount.trim() === "" || isNaN(parsedAmount) || parsedAmount <= 0) {
            setErrorMessage('金額が入力されていません。')
            return;
        }
        if (date === null) {
            setErrorMessage('日付が入力されていません')
            return;
        }
        onAdd({ amount: parsedAmount, type, date, category}); // 親で定義した関数を呼び出すので親に渡すことができる
        setAmount("");
        setType("income");  //  初期化
        setErrorMessage('');
        setDate(null);
    };
    return (
        <>
            <Stack spacing={2}>
                {/* タイプ選択 */}
                <FormControl fullWidth>
                    <InputLabel>タイプ</InputLabel>
                    <Select value={type} onChange={(e) => setType(e.target.value)}>
                        <MenuItem value="income">収入</MenuItem>
                        <MenuItem value="expense">支出</MenuItem>
                    </Select>
                </FormControl>

                <FormControl fullWidth sx={{ mt: 2 }}>
                    <InputLabel>カテゴリ</InputLabel>
                    {type === "income" ? (
                        <Select value={category} onChange={(e) => setCategory(e.target.value)}>
                            <MenuItem value="給与">給与</MenuItem>
                            <MenuItem value="副業">副業</MenuItem>
                            <MenuItem value="投資">投資</MenuItem>
                        </Select>
                    ) : (
                        <Select value={category} onChange={(e) => setCategory(e.target.value)}>
                            <MenuItem value="食費">食費</MenuItem>
                            <MenuItem value="交通費">交通費</MenuItem>
                            <MenuItem value="娯楽費">娯楽費</MenuItem>
                            <MenuItem value="その他">その他</MenuItem>
                        </Select>
                    )}
                </FormControl>

                 <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DatePicker label="日付を選択してください" format="YYYY/MM/DD" value={date} onChange={(newDate) => setDate(newDate)}/>
                </LocalizationProvider>

                {/* 金額入力 */}
                <TextField label="取引" type="number" margin="normal" value={amount} onChange={e => setAmount(e.target.value)} />
                <Typography variant="body1">入力金額:{amount}</Typography>
                <Button variant="contained" color="primary" onClick={handleRegister}>登録</Button>
                {/* <Alert>{errorMessage}</Alert> */}
                {/* エラーメッセージがあるときだけ表示 */}
                {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
            </Stack>
        </>
    )
}