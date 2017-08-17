from .frame_a_view import CHECK_BTN_ENTRY_DIC, DATABASES, BTN_ENTRY_DICT
from pymysql import connect


class Mysql(object):

    def __init__(self,):
        self.db_config = DATABASES

    @property
    def connect(self):
        return connect(host=self.db_config['HOST'],
                       user=self.db_config['USER'],
                       passwd=self.db_config['PASSWORD'],
                       db=self.db_config['NAME'])


def init_btn_entry_val_from_sql():
    """"""
    conn = Mysql().connect
    with conn as cur:
        cur.execute(
            "select equipment_port, equipment_status from i_equipment_io "
            "where equipment_id like 'a%' or equipment_id like 'm%'"
        )
        result_on_off = cur.fetchall()
    for item in result_on_off:
        BTN_ENTRY_DICT[item[0]] = item[1]
    with conn as cur:
        cur.execute(
            "select resource_id, resource_limit from i_resource_limit "
            "where resource_id like 'man_a%' or resource_id like 'man_m%'"
        )
        result_num = cur.fetchall()
        for item in result_num:
            BTN_ENTRY_DICT[item[0]] = int(item[1])
    return BTN_ENTRY_DICT


def update_on_off(cursor, run_arg):
    # equipment_port 需要确定
    for key, value in CHECK_BTN_ENTRY_DIC.items():
        cursor.execute(
            "update i_equipment_io set equipment_status=%s where "
            "equipment_port='%s'" % (value.var.get(), key)
        )
    cursor.execute("update i_equipment_io set inserted_on='%s'" % run_arg)


def insert_package(cursor, num: str, run_arg):
    # ============================ 插入陆侧数据 ===============================
    cursor.execute("truncate i_od_parcel_landside")
    cursor.execute("truncate i_od_small_landside")
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_landside_day "
        "where parcel_type='parcel' "
        "limit %s" % int(int(num) / 2 * 0.88)
    )
    cursor.execute(
        "insert into i_od_parcel_landside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_landside_day "
        "where parcel_type='nc' "
        "limit %s" % int(int(num) / 2 * 0.07)
    )
    cursor.execute(
        "INSERT into i_od_small_landside "
        "(small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, "
        "plate_num, parcel_type, limit_type_code, arrive_time, send_time, "
        "inserted_on, modified_on) "
        "SELECT "
        "small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, "
        "plate_num, parcel_type, limit_type_code, arrive_time, send_time, "
        "inserted_on, modified_on "
        "FROM `i_od_small_landside_day` AS s "
        "WHERE s.`parcel_id` IN "
        "( SELECT DISTINCT t.parcel_id "
        "FROM"
        "( SELECT f.parcel_id "
        "FROM i_od_parcel_landside_day AS f "
        "WHERE f.`parcel_type`='small' "
        "LIMIT %s) AS t)" % int(int(num) / 2 * 0.05)
    )
    # ============================ 插入空侧数据 ===============================
    cursor.execute("truncate i_od_parcel_airside")
    cursor.execute("truncate i_od_small_airside")
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_airside_day "
        "where parcel_type='parcel' "
        "limit %s" % int(int(num) / 2 * 0.88)
    )
    cursor.execute(
        "insert into i_od_parcel_airside "
        "(parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code,"
        " dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "select "
        "parcel_id, src_dist_code, src_type, dest_dist_code, dest_zone_code, "
        "dest_type, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "from i_od_parcel_airside_day "
        "where parcel_type='nc' "
        "limit %s" % int(int(num) / 2 * 0.07)
    )
    cursor.execute(
        "INSERT into i_od_small_airside "
        "(small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, "
        "uld_num, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "SELECT "
        "small_id, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, "
        "uld_num, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "FROM `i_od_small_airside_day` AS s "
        "WHERE s.`parcel_id` IN (SELECT DISTINCT t.parcel_id "
        "FROM(SELECT f.parcel_id FROM i_od_parcel_airside_day AS f "
        "WHERE f.`parcel_type`='small' "
        "LIMIT %s) AS t)" % int(int(num) / 2 * 0.05)
    )
    cursor.execute("update i_od_parcel_landside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_parcel_airside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_small_landside set inserted_on='%s'" % run_arg)
    cursor.execute("update i_od_small_airside set inserted_on='%s'" % run_arg)


def update_person(cursor, run_arg):
    for key, instance in CHECK_BTN_ENTRY_DIC.items():
        cursor.execute("update i_resource_limit set resource_limit={} where "
                       "resource_id='{}'".format(
            instance.string_combobox.get(), 'man_' + key)
        )
    cursor.execute("update i_resource_limit set inserted_on='%s'" % run_arg)


def read_result(cursor):
    cursor.execute(
        "select min(cast(real_time_stamp as datetime)), "
        "max(cast(real_time_stamp as datetime)) from o_machine_table where "
        "action='wait' and equipment_id like 'a%'")

    fast_time, later_time = cursor.fetchone()
    cursor.execute(
        "select "
        "max(cast(real_time_stamp as datetime)), "
        "(max(time_stamp)-min(time_stamp))/3600 "
        "from o_machine_table "
        "where action='wait'"
    )
    last_solve_time, total_solve_time = cursor.fetchone()
    return {
        'fast_time': fast_time,
        'later_time': later_time,
        'last_solve_time': last_solve_time,
        'total_solve_time': total_solve_time
    }


def save_to_past_run(cursor):
    cursor.execute(
        "insert into i_equipment_io_past_run "
        "(run_time, equipment_port, equipment_id, process_time, "
        "allocate_rule, equipment_status, inserted_on, modified_on) "
        "select "
        "inserted_on, equipment_port, equipment_id, process_time, "
        "allocate_rule, equipment_status, inserted_on, modified_on "
        "from i_equipment_io"
    )

    cursor.execute(
        "insert into i_od_parcel_landside_past_run "
        "(run_time, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, plate_num, parcel_type, "
        "limit_type_code, arrive_time, send_time, inserted_on, modified_on) "
        "select "
        "inserted_on, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, plate_num, parcel_type, "
        "limit_type_code, arrive_time, send_time, inserted_on, modified_on "
        "from i_od_parcel_landside"
    )

    cursor.execute(
        "insert into i_od_parcel_airside_past_run "
        "(run_time, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, plate_num, parcel_type, limit_type_code, "
        "arrive_time, send_time, inserted_on, modified_on) "
        "select "
        "inserted_on, parcel_id, src_dist_code, src_type, dest_dist_code, "
        "dest_zone_code, dest_type, plate_num, parcel_type, limit_type_code, "
        "arrive_time, send_time, inserted_on, modified_on "
        "from i_od_parcel_airside"
    )

    cursor.execute(
        "INSERT into i_od_small_landside_past_run "
        "(run_time, small_id, parcel_id, src_dist_code, src_type, "
        "dest_dist_code, dest_zone_code, dest_type, "
        "plate_num, parcel_type, limit_type_code, arrive_time, send_time, "
        "inserted_on, modified_on) "
        "SELECT "
        "inserted_on, small_id, parcel_id, src_dist_code, src_type, "
        "dest_dist_code, dest_zone_code, dest_type, "
        "plate_num, parcel_type, limit_type_code, arrive_time, send_time, "
        "inserted_on, modified_on "
        "FROM i_od_small_landside"
    )

    cursor.execute(
        "INSERT into i_od_small_airside_past_run "
        "(run_time, small_id, parcel_id, src_dist_code, src_type, "
        "dest_dist_code, dest_zone_code, dest_type, "
        "uld_num, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on) "
        "SELECT "
        "inserted_on, small_id, parcel_id, src_dist_code, src_type, "
        "dest_dist_code, dest_zone_code, dest_type, "
        "uld_num, plate_num, parcel_type, limit_type_code, arrive_time, "
        "send_time, inserted_on, modified_on "
        "FROM i_od_small_airside"
    )

    cursor.execute(
        "insert into i_resource_limit_past_run "
        "(run_time, resource_id, resource_name, resource_limit, "
        "capacity_per_resource, resource_on_number, resource_number, "
        "inserted_on, modified_on) "
        "select "
        "inserted_on, resource_id, resource_name, resource_limit, "
        "capacity_per_resource, resource_on_number, resource_number, "
        "inserted_on, modified_on "
        "from i_resource_limit"
    )

    cursor.execute(
        "insert into o_truck_table_past_run "
        "(equipment_id, truck_id, truck_type, time_stamp, action, store_size, "
        "real_time_stamp, run_time) "
        "select "
        "equipment_id, truck_id, truck_type, time_stamp, action, store_size, "
        "real_time_stamp, run_time "
        "from o_truck_table"
    )

    cursor.execute(
        "insert into o_pipeline_table_past_run "
        "(pipeline_id, queue_id, parcel_id, small_id, parcel_type, time_stamp, "
        "action, real_time_stamp, run_time)"
        "select "
        "pipeline_id, queue_id, parcel_id, small_id, parcel_type, time_stamp, "
        "action, real_time_stamp, run_time "
        "from o_pipeline_table"
    )

    cursor.execute(
        "insert into o_machine_table_past_run "
        "(equipment_id, parcel_id, small_id, parcel_type, time_stamp, action, "
        "real_time_stamp, run_time) "
        "select "
        "equipment_id, parcel_id, small_id, parcel_type, time_stamp, action, "
        "real_time_stamp, run_time "
        "from o_machine_table"
    )


def delete_index(cursor):
    cursor.execute("drop index ix_o_machine_run_time_packageid on "
                   "o_machine_table;")

    cursor.execute("drop index ix_o_machine_table_equipment_id on "
                   "o_machine_table;")

    cursor.execute("drop index ix_o_pipeline_run_time_packageid on "
                   "o_pipeline_table;")


def create_index(cursor):
    cursor.execute("create index ix_o_machine_run_time_packageid on "
                   "o_machine_table (`package_id`)")

    cursor.execute("create index ix_o_machine_table_equipment_id on "
                   "o_machine_table (`equipment_id`)")

    cursor.execute("create index ix_o_pipeline_run_time_packageid on "
                   "o_pipeline_table(`package_id`)")
