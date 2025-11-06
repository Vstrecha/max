import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://pahounjxyjvchqcucrkw.supabase.co'
const supabaseKey = 'sb_publishable_WA9u31awG9sHeKEUIMhh5g_6keVJVo_'
const supabase = createClient(supabaseUrl, supabaseKey)

export { supabase }
