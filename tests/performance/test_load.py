import threading
import time


def test_concurrent_screener_requests(client):

    times = []

    lock = threading.Lock()

    def worker():

        start = time.perf_counter()

        response = client.get("/api/v1/screener")

        elapsed = time.perf_counter() - start

        assert response.status_code == 200

        with lock:
            times.append(elapsed)

    threads = []

    overall_start = time.perf_counter()

    for _ in range(10):

        t = threading.Thread(target=worker)

        threads.append(t)

        t.start()

    for t in threads:
        t.join()

    overall = time.perf_counter() - overall_start

    print(f"\nOverall: {overall:.3f}s")
    print(f"Average: {sum(times)/len(times):.3f}s")
    print(f"Maximum: {max(times):.3f}s")

    assert len(times) == 10
    assert overall < 10
