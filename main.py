import machine, sys
import display_app
try:
    display_app.main()
except Exception as e:
    print("Fatal error in main:")
    sys.print_exception(e)
