from SICAR import Sicar, OutputFormat, State
from multiprocessing import Pool, Queue
from functools import partial
import pprint

def download_parallel(city_code, *args, **kwargs):
    """Takes download_city_code arguments"""
    car = queue.get()
    path = car.download_city_code(city_code=city_code, **kwargs)
    queue.put(car)
    return (city_code, path)


def initQueue(queue: Queue):
    queue.put(Sicar(email="sicar@sicar.com"))


if __name__ == "__main__":
    # Replace state
    state = State.RR

    queue = Queue()
    base = Sicar(email="sicar@sicar.com")
    cities_codes = base.get_cities_codes(state=state)

    # processes is the number of worker processes to use. If processes is None then the number returned by os.cpu_count() is used.
    with Pool(processes=4, initializer=initQueue, initargs=(queue,)) as pool:
        result = pool.map(
            partial(
                download_parallel,
                folder=f"drive/MyDrive/SICAR/{state}_Parallel"
            ),
            cities_codes.values(),
        )
        pprint.pprint(result)
