// import React from "react";

// function Users() {
//   return <h1>👤 사용자 관리 페이지</h1>;
// }

// export default Users;


import React, { useEffect, useState } from "react";

function Users() {
  const [users, setUsers] = useState([]);
  const [name, setName] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [identifierCode, setIdentifierCode] = useState("");

  // 사용자 목록 불러오기
  const fetchUsers = () => {
    fetch("http://localhost:3434/users")
      .then((res) => res.json())
      .then((data) => setUsers(data.users))
      .catch((err) => console.error("사용자 불러오기 실패", err));
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // 사용자 추가
  const handleAddUser = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("name", name);
    formData.append("birth_date", birthDate);
    formData.append("identifier_code", identifierCode);

    fetch("http://localhost:3434/users", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then(() => {
        setName("");
        setBirthDate("");
        setIdentifierCode("");
        fetchUsers(); // 목록 새로고침
      })
      .catch((err) => console.error("사용자 추가 실패", err));
  };

  // 사용자 삭제
  const handleDeleteUser = (userId) => {
    fetch(`http://localhost:3434/users/${userId}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then(() => {
        fetchUsers(); // 목록 새로고침
      })
      .catch((err) => console.error("사용자 삭제 실패", err));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>👤 사용자 관리 페이지</h1>

      {/* 사용자 추가 폼 */}
      <form onSubmit={handleAddUser} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="이름"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="date"
          placeholder="생년월일"
          value={birthDate}
          onChange={(e) => setBirthDate(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="식별코드"
          value={identifierCode}
          onChange={(e) => setIdentifierCode(e.target.value)}
          required
        />
        <button type="submit">➕ 추가</button>
      </form>

      {/* 사용자 목록 */}
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>ID</th>
            <th>이름</th>
            <th>생년월일</th>
            <th>식별코드</th>
            <th>삭제</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.user_id}>
              <td>{u.user_id}</td>
              <td>{u.name}</td>
              <td>{u.birth_date}</td>
              <td>{u.identifier_code}</td>
              <td>
                <button onClick={() => handleDeleteUser(u.user_id)}>❌</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Users;

