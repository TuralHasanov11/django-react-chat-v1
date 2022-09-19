import React, { useEffect, useState } from 'react'
import { Avatar, Button, Card, CardHeader, Container, createTheme, CssBaseline, Grid, Link, Paper, TextField, ThemeProvider, Typography } from '@mui/material';
import {w3cwebsocket as W3CWebsocet} from "websocket"
import { purple, teal } from '@mui/material/colors';


const theme = createTheme({
  palette: {
    chat: {
      sender: purple[50],
      receiver: teal[50],
    },
    secondary: {
      main: '#f44336',
    },
  }
});

export default function Chat() {

    const [isAuth, setIsAuth] = useState(false)
    const [messages, setMessages] = useState([])
    const [messageInput, setMessageInput] = useState("")
    const [username, setUsername] = useState("")
    const [room, setRoom] = useState("room123")

    const client = new W3CWebsocet("ws://127.0.0.1:8000/ws/chat/"+room+"/")

    useEffect(()=>{
        client.onopen = () => {
            console.log("Websocket client connected")
        }

        client.onmessage = (msg) => {
            const data = JSON.parse(msg.data)
            if(data){
                setMessages(prevMessages => {
                    return [...prevMessages, {message: data.message, username: data.username}]
                })
            }
        }
    }, [])

    function submitForm(e){
        e.preventDefault()
        client.send(JSON.stringify({
            type:"message",
            message: messageInput,
            username
        }))

        setMessageInput("")
    }


  return (
    <ThemeProvider theme={theme}>
      <Container>
        {
          isAuth 
          ?
          <div style={{ marginTop: 50, }}>
           <Typography component="h1" variant="h5">
             Room Name: {room}
           </Typography>
            <Paper style={{ height: 500, maxHeight: 500, overflow: 'auto', boxShadow: 'none', }}>
              {messages.map((message, index) => <>
                <Card
                  key={index} 
                  variant="outlined"
                  sx={{
                    margin: theme.spacing(1),
                    bgcolor: message.username === username ? "chat.sender" : "chat.receiver",
                    boxShadow: 'none',  
                    justifyContent: message.username === username ? "flex-start" : "flex-end",
                  }}>
                  <CardHeader
                    avatar={
                      <Avatar sx={{
                        margin: theme.spacing(1),
                        backgroundColor: theme.palette.secondary.main,
                      }}>
                        {message.username[0].toUpperCase()}
                      </Avatar>
                    }
                    title={message.name}
                    subheader={message.message}
                  />
                </Card>
              </>)}
            </Paper>

            <form sx={{
                    width: '100%', // Fix IE 11 issue.
                    marginTop: theme.spacing(1),
                }} noValidate onSubmit={submitForm}>
              <TextField
                id="outlined-helperText"
                label="Make a comment"
                variant="outlined"
                value={messageInput}
                fullWidth
                onChange={e => {
                    setMessageInput(e.target.value);
                }}
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                sx={{
                    margin: theme.spacing(3, 0, 2),
                  }}
              >
                Start Chatting
                </Button>
            </form>
          </div> 
          : 
        <div>
            <CssBaseline />
            <div sx={{
                marginTop: theme.spacing(8),
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}>
                <Typography component="h1" variant="h5">
                    ChattyRooms
                </Typography>
                <form sx={{
                    width: '100%', // Fix IE 11 issue.
                    marginTop: theme.spacing(1),
                }} noValidate onSubmit={value => setIsAuth(true)}>
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label="Chatroom Name"
                        name="Chatroom Name"
                        autoFocus
                        value={room}
                        onChange={e => { 
                            setRoom(e.target.value);
                        }}
                    />
                    <TextField
                        variant="outlined"
                        margin="normal"
                        required
                        fullWidth
                        name="Username"
                        label="Username"
                        type="Username"
                        id="Username"
                        value={username}
                        onChange={e => {
                            setUsername(e.target.value);
                        }}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        sx={{
                            margin: theme.spacing(3, 0, 2),
                          }}
                        >
                        Start Chatting
                    </Button>
                    <Grid container>
                        <Grid item xs>
                            <Link href="#" variant="body2">
                            Forgot password?
                            </Link>
                        </Grid>
                        <Grid item>
                            <Link href="#" variant="body2">
                            {"Don't have an account? Sign Up"}
                            </Link>
                        </Grid>
                    </Grid>
                </form>
            </div>
        </div>
        }
    </Container>
    </ThemeProvider>
  )
}
 