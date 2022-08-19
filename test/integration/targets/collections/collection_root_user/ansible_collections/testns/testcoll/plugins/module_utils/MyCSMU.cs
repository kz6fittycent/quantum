using System;

using quantum_collections.testns.testcoll.plugins.module_utils.AnotherCSMU;
using quantum_collections.testns.testcoll.plugins.module_utils.subpkg.subcs;

//TypeAccelerator -Name MyCSMU -TypeName CustomThing

namespace quantum_collections.testns.testcoll.plugins.module_utils.MyCSMU
{
    public class CustomThing
    {
        public static string HelloWorld()
        {
            string res1 = AnotherThing.CallMe();
            string res2 = NestedUtil.HelloWorld();
            return String.Format("Hello from user_mu collection-hosted MyCSMU, also {0} and {1}", res1, res2);
        }
    }
}
