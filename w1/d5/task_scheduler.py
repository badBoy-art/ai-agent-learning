import asyncio
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class TaskStatus(Enum):
    PENDING = "等待中"
    RUNNING = "运行中"
    COMPLETED = "已完成"
    FAILED = "失败"
    CANCELLED = "已取消"


@dataclass
class TaskResult:
    task_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    @property
    def duration(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


class AsyncTask:
    def __init__(self, task_id: str, func: Callable, *args,
                 dependencies: List[str] = None, max_retries: int = 0):
        self.task_id = task_id
        self.func = func
        self.args = args
        self.dependencies = dependencies or []
        self.max_retries = max_retries
        self.status = TaskStatus.PENDING
        self.result: Optional[TaskResult] = None
        self._current_retry = 0

    async def execute(self) -> TaskResult:
        self.status = TaskStatus.RUNNING
        start_time = datetime.now()

        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(self.func):
                    result = await self.func(*self.args)
                else:
                    result = self.func(*self.args)

                self.status = TaskStatus.COMPLETED
                self.result = TaskResult(
                    task_id=self.task_id,
                    status=TaskStatus.COMPLETED,
                    result=result,
                    start_time=start_time,
                    end_time=datetime.now()
                )
                return self.result

            except Exception as e:
                if attempt < self.max_retries:
                    await asyncio.sleep(1)  # 重试前等待
                    continue
                else:
                    self.status = TaskStatus.FAILED
                    self.result = TaskResult(
                        task_id=self.task_id,
                        status=TaskStatus.FAILED,
                        error=str(e),
                        start_time=start_time,
                        end_time=datetime.now()
                    )
                    return self.result

    def __str__(self) -> str:
        return f"任务({self.task_id}, {self.status.value})"


class AsyncTaskScheduler:
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.tasks: Dict[str, AsyncTask] = {}
        self.completed: Dict[str, TaskResult] = {}
        self._semaphore = asyncio.Semaphore(max_concurrent)

    def add_task(self, task: AsyncTask) -> None:
        if task.task_id in self.tasks:
            raise ValueError(f"任务ID {task.task_id} 已存在")
        self.tasks[task.task_id] = task

    def _check_dependencies(self, task: AsyncTask) -> bool:
        for dep_id in task.dependencies:
            if dep_id not in self.completed:
                return False
            if self.completed[dep_id].status != TaskStatus.COMPLETED:
                return False
        return True

    async def _execute_task(self, task: AsyncTask) -> None:
        async with self._semaphore:
            # 等待依赖完成
            while not self._check_dependencies(task):
                await asyncio.sleep(0.1)

            # 执行任务
            result = await task.execute()
            self.completed[task.task_id] = result

            status_icon = "✓" if result.status == TaskStatus.COMPLETED else "✗"
            print(f"{status_icon} {task.task_id}: {result.status.value}")

    async def run_all(self) -> Dict[str, TaskResult]:
        # 按依赖关系排序
        sorted_tasks = self._topological_sort()

        # 并发执行
        tasks_to_run = [self._execute_task(task) for task in sorted_tasks]
        await asyncio.gather(*tasks_to_run, return_exceptions=True)

        return self.completed

    def _topological_sort(self) -> List[AsyncTask]:
        # 简单的拓扑排序
        result = []
        visited = set()

        def visit(task_id: str):
            if task_id in visited:
                return
            visited.add(task_id)

            task = self.tasks.get(task_id)
            if task:
                for dep_id in task.dependencies:
                    visit(dep_id)
                result.append(task)

        for task_id in self.tasks:
            visit(task_id)

        return result

    def get_results(self) -> Dict[str, TaskResult]:
        return self.completed

    def get_statistics(self) -> Dict:
        total = len(self.completed)
        completed = sum(1 for r in self.completed.values()
                        if r.status == TaskStatus.COMPLETED)
        failed = sum(1 for r in self.completed.values()
                     if r.status == TaskStatus.FAILED)

        durations = [r.duration for r in self.completed.values()
                     if r.duration is not None]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total": total,
            "completed": completed,
            "failed": failed,
            "avg_duration": avg_duration
        }
