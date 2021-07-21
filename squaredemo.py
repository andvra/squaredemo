from app1 import App1
from app2 import App2

if __name__ == "__main__":
    app1 = App1()
    app1.on_test_performance()
    # app2 = App2()
    # app2.on_execute()

    # TOOD: Figure out; how much time is spent on calculations vs. drawing the squares?
    # Easy to check; set angle to pi/4 and comment out the rendering part. What is the time consumed?
    #   Uncomment the rendering. What is the time consumed now?
