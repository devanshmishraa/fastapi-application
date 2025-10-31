
from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "Posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    fie_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield







"""
## 1️⃣ Sync vs Async (simplest explanation)

* **Sync (Synchronous)** = “One thing at a time.”

Example:

```python
print("Start")
print("Wait 5 seconds…")
time.sleep(5)  # blocks everything
print("End")
```

* The program **stops and waits** until the task is done before moving on.

* **Async (Asynchronous)** = “Do things in the background without stopping.”

Example:

```python
import asyncio

async def wait():
    print("Start waiting")
    await asyncio.sleep(5)  # doesn’t block other things
    print("Done waiting")
```

* The program can do other stuff while waiting for a slow task (like talking to a database or web request).

**Bottom line:**

* Async = non-blocking. Sync = blocking.

---

## 2️⃣ Back to your code

### `engine = create_async_engine(DATABASE_URL)`

* Think of `engine` as your **connection to the database**.
* Async engine = it **can talk to the database without stopping your program** while waiting for a response.
* Sync engine = it **waits for the database** and blocks your program.

---

### `async_session_maker = async_sessionmaker(engine, expire_on_commit=False)`

* A **session** is like a **workspace** to do things in your database (query, add, delete).
* `async_sessionmaker` = a **factory that produces sessions** for you.
* Using it with async means you can do database stuff **without freezing your program**.

Analogy:

> Imagine a café. `engine` is the café itself, and `async_session_maker` is the barista who prepares your coffee workspace. You can “order coffee” without stopping other customers from being served.

---

### `async def create_db_and_tables():`

```python
async with engine.begin() as conn:
    await conn.run_sync(DeclarativeBase.metadata.create_all)
```

Step by step:

1. `async with engine.begin() as conn:` → “Open a table-building session in the database.”
2. `await conn.run_sync(...)` → “Tell the database: create tables based on my models.”

* `async` and `await` = keywords that tell Python: “This may take time, don’t block everything else while waiting.”
* Without async, the program would **stop everything else until the tables are created**.

---

### `async def get_async_session() -> AsyncGenerator[AsyncSession, None]:`

```python
async with async_session_maker() as session:
    yield session
```

* **What it does:**

  1. Creates a **database workspace** (session).
  2. Gives it to your code when you need it (`yield`).
  3. Automatically **closes it when done**.

Analogy:

> Think of it like borrowing a library book. You take the book (session), read it (do your queries), and then it’s returned automatically when you’re done.

* `AsyncGenerator` just tells Python: “I will **give something temporarily**, and I might do it asynchronously.”

---

### 3️⃣ Putting it all together in “normal words”

1. **Engine:** The database building itself.
2. **Session maker:** Someone who gives you a workspace in the database.
3. **create_db_and_tables:** Build all the tables so the database knows where to store posts.
4. **get_async_session:** Give a workspace for your API route to use, and clean up automatically.
5. **Async:** Makes sure your program can keep running **other tasks while waiting for the database**.

---

💡 **Key takeaway:**

Even if you don’t fully understand async yet, think **step by step**:

1. Build the database → `create_db_and_tables()`
2. Connect to the database → `engine`
3. Get a workspace → `get_async_session()`
4. Do stuff in workspace → add, read, delete posts

Async just **prevents your FastAPI server from getting stuck** while it’s talking to the database.

---
"""