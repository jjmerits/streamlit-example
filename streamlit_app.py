from SessionState import get

session_state = get(password='')

if session_state.password != 'pwd123':
    pwd_placeholder = st.sidebar.empty()
    pwd = pwd_placeholder.text_input("Password:", value="", type="password")
    session_state.password = pwd
    if session_state.password == 'pwd123':
        pwd_placeholder.empty()
        main()
    else:
        st.error("the password you entered is incorrect")
else:
    main()
