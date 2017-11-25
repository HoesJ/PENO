import multiprocessing
import time, math

import ReadObj_
import ViewFactor

def print_starting(length, N, num_processes):
    print("\nCalculating view factors...")
    expected_time = (length**2)*N*0.0018 / num_processes

    days = math.floor(expected_time / 86400)
    remaining = expected_time - days * 86400
    hours = math.floor(remaining / 3600)
    remaining -= hours * 3600
    minutes = math.floor(remaining / 60)
    remaining -= minutes * 60
    seconds = int(remaining)
    print("Expected time: {0} --- {1} days, {2} hours, {3} minutes, {4} seconds".format(expected_time, days, hours, minutes, seconds))
    return

def run(all_faces, N, num_processes, start=0, end=None):
    if (end == None):
        end = len(all_faces)
    print_starting(end-start, N, num_processes)

    start_time = time.perf_counter()
    
    processes = list()
    recievers = list()
    to_do = end-start
    step = int(to_do/num_processes)

    for i in range(num_processes):
        start_index = i * step
        end_index = (i+1) * step if i < num_processes-1 else to_do

        recieving, sending = multiprocessing.Pipe(False)
        p = multiprocessing.Process(target=ViewFactor.run_everything, args=(all_faces, start_index, end_index, N, sending))
        p.start()
        processes.append(p)
        recievers.append(recieving)

    # Wait for result
    result = list()
    for reciever in recievers:
        from_process = reciever.recv()
        result.extend(from_process)

    # Just to be sure
    for p in processes:
        p.join()

    ViewFactor.Export(result, time=time.perf_counter()-start_time)


if __name__ == "__main__":
    ReadObj_.SetFile("mesh_bungalow.obj")
    ReadObj_.GetAllInfo()
    run(ReadObj_.GetAllFaces(), 3, 2)